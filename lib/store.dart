import 'dart:async';
import 'dart:convert';
import 'dart:math';
import 'package:flutter/foundation.dart';
import 'package:flutter/services.dart';
import 'model.dart';

abstract class Persistence {
  Future<String?> read();
  Future<void> write(String value);
}

class DevicePersistence implements Persistence {
  static const channel = MethodChannel('com.gritpractice.grit/storage');
  @override
  Future<String?> read() => channel.invokeMethod<String>('read');
  @override
  Future<void> write(String value) =>
      channel.invokeMethod<void>('write', value);
}

class AppController extends ChangeNotifier {
  final Persistence persistence;
  AppController(this.persistence);
  List<PracticeSession> records = [];
  PracticeSession? active;
  String? error;
  bool loadFailed = false;
  Future<void> _tail = Future.value();
  bool _disposed = false;
  Future<void> _settled = Future.value();
  bool _changing = false;
  @override
  void notifyListeners() {
    if (!_disposed) super.notifyListeners();
  }

  Future<void> load() async {
    try {
      final raw = await persistence.read();
      if (raw != null) {
        final data = decode(raw);
        records = data.$1;
        active =
            null; // Unfinished legacy sessions are intentionally not resumed.
      }
      error = null;
      loadFailed = false;
    } catch (_) {
      error = '저장된 기록을 읽지 못했어요. 원본은 그대로 보존되어 있어요.';
      loadFailed = true;
    }
    notifyListeners();
  }

  static (List<PracticeSession>, PracticeSession?) decode(String raw) {
    final root = jsonDecode(raw) as Map<String, dynamic>;
    if (root['app'] != 'GRIT' || root['format'] != 1) {
      throw const FormatException('지원하지 않는 GRIT 기록 형식입니다.');
    }
    final items = (root['records'] as List)
        .map(
          (r) => PracticeSession.fromJson(Map<String, dynamic>.from(r as Map)),
        )
        .toList();
    if (items.any((r) => r.completedAt == null) ||
        items.map((r) => r.id).toSet().length != items.length) {
      throw const FormatException('잘못된 완료 기록');
    }
    items.sort((a, b) => b.completedAt!.compareTo(a.completedAt!));
    return (items, null);
  }

  String encode({
    List<PracticeSession>? history,
    PracticeSession? current,
    bool omitActive = false,
  }) => jsonEncode({
    'app': 'GRIT',
    'format': 1,
    'records': (history ?? records).map((r) => r.toJson()).toList(),
    'active': null,
  });
  Future<void> _write(String data) {
    final next = _tail.then((_) => persistence.write(data));
    _tail = next.then<void>((_) {}, onError: (Object e, StackTrace s) {});
    return next;
  }

  Future<void> _change(String data, VoidCallback commit) async {
    if (_changing) throw StateError('기록 저장 중입니다.');
    _changing = true;
    final settled = Completer<void>();
    _settled = settled.future;
    try {
      await _write(data);
      commit();
    } finally {
      _changing = false;
      settled.complete();
    }
  }

  Future<void> flush() async {
    await _settled;
    if (loadFailed) return;
    try {
      await _write(encode());
      error = null;
    } catch (_) {
      error = '저장하지 못했어요. 공간을 확인하고 다시 시도해 주세요.';
      rethrow;
    } finally {
      notifyListeners();
    }
  }

  Future<PracticeSession> start(SetKind kind) async {
    if (loadFailed) throw StateError('기록을 읽을 수 없습니다.');
    if (active != null) throw StateError('이미 연습 중입니다.');
    final seed = Random.secure().nextInt(0x7fffffff);
    final problems = Generator(seed).generate(kind);
    final now = DateTime.now();
    final session = PracticeSession(
      id: '${now.microsecondsSinceEpoch}-$seed',
      kind: kind,
      seed: seed,
      problems: problems,
      startedAt: now,
    );
    active = session;
    notifyListeners();
    return session;
  }

  void answer(String key, String value) {
    final session = active;
    if (session == null) return;
    session.answers[key] = value;
    notifyListeners();
  }

  void memo(String key, String value) {
    final session = active;
    if (session == null || !session.memoKeys.contains(key)) return;
    if (value.isEmpty) {
      session.memos.remove(key);
    } else {
      session.memos[key] = value;
    }
    notifyListeners();
  }

  void page(int value) {
    active?.page = value;
  }

  Future<PracticeSession> complete(DateTime endedAt) async {
    final session = active;
    if (session == null) throw StateError('진행 중인 연습이 없습니다.');
    final completed = PracticeSession.fromJson(session.toJson());
    completed.elapsedSeconds = completed.elapsedAt(endedAt);
    completed.completedAt = endedAt;
    final next = [completed, ...records];
    await _change(encode(history: next, omitActive: true), () {
      records = next;
      active = null;
      error = null;
    });
    notifyListeners();
    return completed;
  }

  Future<void> abandon() async {
    if (_changing) throw StateError('기록 저장 중입니다.');
    active = null;
    notifyListeners();
  }

  Future<void> resetHistory() async {
    if (loadFailed) throw StateError('기록을 읽을 수 없습니다.');
    await _change(encode(history: []), () {
      records = [];
      error = null;
    });
    notifyListeners();
  }

  @override
  void dispose() {
    _disposed = true;
    super.dispose();
  }
}
