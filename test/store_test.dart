import 'dart:async';
import 'dart:convert';
import 'package:flutter_test/flutter_test.dart';
import 'package:grit/model.dart';
import 'package:grit/store.dart';

class MemoryPersistence implements Persistence {
  String? value;
  bool fail = false;
  @override
  Future<String?> read() async => value;
  @override
  Future<void> write(String data) async {
    if (fail) throw StateError('disk full');
    value = data;
  }
}

void main() {
  test(
    'background intervals are excluded from completed and reloaded time',
    () async {
      final disk = MemoryPersistence();
      final c = AppController(disk);
      final session = await c.start(SetKind.addition);
      final start = session.startedAt;
      session.pauseTiming(start.add(const Duration(milliseconds: 1250)));
      // Repeated inactive/hidden/paused notifications must not restart the pause.
      session.pauseTiming(start.add(const Duration(seconds: 2)));
      expect(session.elapsedAt(start.add(const Duration(minutes: 20))), 1);
      session.resumeTiming(start.add(const Duration(seconds: 61)));
      session.pauseTiming(start.add(const Duration(milliseconds: 61750)));
      session.resumeTiming(start.add(const Duration(milliseconds: 120250)));
      // 1.25 + .75 + 1.5 foreground seconds, rounded once at the end.
      final done = await c.complete(
        start.add(const Duration(milliseconds: 121750)),
      );
      expect(done.elapsedSeconds, 3);
      final reopened = AppController(disk);
      await reopened.load();
      expect(reopened.records.single.elapsedSeconds, 3);
      expect(reopened.records.single.startedAt, start);
      expect(reopened.active, isNull);
      c.dispose();
      reopened.dispose();
    },
  );

  test(
    'unfinished work stays only in memory; completion preserves review and memo',
    () async {
      final disk = MemoryPersistence();
      final c = AppController(disk);
      final session = await c.start(SetKind.addition);
      c.memo('0:r:0', '456');
      c.memo('4:c:6', '-');
      c.memo('4:r:5', '-123');
      final key = session.expected.keys.first;
      c.answer(key, session.expected[key]!);
      c.page(3);
      await c.flush();
      final restarted = AppController(disk);
      await restarted.load();
      expect(restarted.active, isNull);
      expect(restarted.records, isEmpty);
      expect(session.answered, 1);
      expect(session.correct, 1);
      final done = await c.complete(
        session.startedAt.add(const Duration(seconds: 187)),
      );
      expect(done.memos, session.memos);
      expect(done.correct, 1);
      final reopened = AppController(disk);
      await reopened.load();
      expect(reopened.active, isNull);
      expect(reopened.records.single.memos, session.memos);
      expect(reopened.records.single.answers, session.answers);
      expect(reopened.records.single.elapsedSeconds, 187);
      expect(reopened.records.single.startedAt, session.startedAt);
      expect(
        reopened.records.single.problems.first.values,
        session.problems.first.values,
      );
      c.dispose();
      restarted.dispose();
      reopened.dispose();
    },
  );
  test('legacy active is ignored while completed records remain', () async {
    final disk = MemoryPersistence();
    final c = AppController(disk);
    await c.start(SetKind.division);
    await c.complete(DateTime.now());
    final active = await c.start(SetKind.addition);
    final root = jsonDecode(c.encode()) as Map<String, dynamic>;
    root['active'] = active.toJson();
    disk.value = jsonEncode(root);
    final reopened = AppController(disk);
    await reopened.load();
    expect(reopened.loadFailed, isFalse);
    expect(reopened.active, isNull);
    expect(reopened.records.length, 1);
    await reopened.flush();
    expect(jsonDecode(disk.value!)['active'], isNull);
    c.dispose();
    reopened.dispose();
  });
  test(
    'legacy completed memo omission loads and corrupt completed memo is protected',
    () async {
      final disk = MemoryPersistence();
      final c = AppController(disk);
      await c.start(SetKind.addition);
      final done = await c.complete(DateTime.now());
      final legacy = done.toJson()..remove('memos');
      expect(PracticeSession.fromJson(legacy).memos, isEmpty);
      for (final bad in [
        {'0:r:99': '123'},
        {'0:r:0': '1234567'},
      ]) {
        final root = jsonDecode(c.encode()) as Map<String, dynamic>;
        root['records'][0]['memos'] = bad;
        final raw = jsonEncode(root);
        disk.value = raw;
        final broken = AppController(disk);
        await broken.load();
        expect(broken.loadFailed, isTrue);
        await broken.flush();
        await expectLater(broken.resetHistory(), throwsStateError);
        expect(disk.value, raw);
        broken.dispose();
      }
      c.dispose();
    },
  );
  test(
    'abandon drops answers and memos but preserves completed history even with full disk',
    () async {
      final disk = MemoryPersistence();
      final c = AppController(disk);
      await c.start(SetKind.multiplication);
      await c.complete(DateTime.now());
      final saved = disk.value;
      await c.start(SetKind.addition);
      c.memo('0:r:0', '456');
      c.answer('0', '123');
      disk.fail = true;
      await c.abandon();
      expect(c.active, isNull);
      expect(c.records.length, 1);
      expect(disk.value, saved);
      c.dispose();
    },
  );
  test(
    'failed completion keeps current answers; retry makes exactly one record',
    () async {
      final disk = MemoryPersistence();
      final c = AppController(disk);
      final session = await c.start(SetKind.multiplication);
      c.answer('0', '>');
      disk.fail = true;
      await expectLater(c.complete(DateTime.now()), throwsStateError);
      expect(c.active, same(session));
      expect(session.completedAt, isNull);
      expect(c.records, isEmpty);
      disk.fail = false;
      await c.complete(DateTime.now());
      expect(c.records.length, 1);
      await expectLater(c.complete(DateTime.now()), throwsStateError);
      expect(c.records.length, 1);
      c.dispose();
    },
  );
  test(
    'reset persists empty history, retains memory only active state',
    () async {
      final disk = MemoryPersistence();
      final c = AppController(disk);
      for (final kind in SetKind.values) {
        await c.start(kind);
        await c.complete(DateTime.now());
      }
      final active = await c.start(SetKind.addition);
      c.memo('0:r:0', '456');
      await c.resetHistory();
      expect(c.records, isEmpty);
      expect(c.active, same(active));
      expect(c.active!.memos['0:r:0'], '456');
      final reopened = AppController(disk);
      await reopened.load();
      expect(reopened.records, isEmpty);
      expect(reopened.active, isNull);
      c.dispose();
      reopened.dispose();
    },
  );
  test('failed reset preserves records and original disk', () async {
    final disk = MemoryPersistence();
    final c = AppController(disk);
    await c.start(SetKind.division);
    await c.complete(DateTime.now());
    final saved = disk.value;
    disk.fail = true;
    await expectLater(c.resetHistory(), throwsStateError);
    expect(c.records.length, 1);
    expect(disk.value, saved);
    c.dispose();
  });
  test('corrupt existing file is never silently replaced', () async {
    final disk = MemoryPersistence()..value = 'bad json';
    final c = AppController(disk);
    await c.load();
    expect(c.loadFailed, isTrue);
    await c.flush();
    await expectLater(c.start(SetKind.addition), throwsStateError);
    expect(disk.value, 'bad json');
    c.dispose();
  });
  test('background flush cannot overwrite a completion transaction', () async {
    final disk = SlowPersistence();
    final c = AppController(disk);
    await c.start(SetKind.multiplication);
    c.answer('0', '>');
    disk.gate = Completer<void>();
    final completion = c.complete(DateTime.now());
    final background = c.flush();
    disk.gate!.complete();
    await completion;
    await background;
    final loaded = AppController.decode(disk.value!);
    expect(loaded.$1.length, 1);
    expect(loaded.$2, isNull);
    c.dispose();
  });
}

class SlowPersistence extends MemoryPersistence {
  Completer<void>? gate;
  @override
  Future<void> write(String data) async {
    if (gate != null) await gate!.future;
    await super.write(data);
  }
}
