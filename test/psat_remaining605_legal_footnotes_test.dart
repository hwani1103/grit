import 'package:flutter_test/flutter_test.dart';
import 'package:grit/psat_sets.dart';
import 'package:grit/psat_text.dart' as current;
import '../artifacts/psat_remaining605_20261030/renderer-footnotes36/psat_text-before.dart'
    as before;

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  test('explicit legal footnotes preserve all900 text and unrelated blocks', () async {
    final catalog = await loadPsatCatalog();
    const affected = {
      'kr-mpm-2026-03-07-psat-s-05',
      'kr-mpm-2025-03-08-psat-s-23',
    };
    final changed = <String>{};
    expect(catalog.questions.length, 900);
    String normalized(List<String> blocks) => blocks.join().replaceAll(RegExp(r'\s+'), '');
    for (final q in catalog.questions.values) {
      final oldBlocks = before.psatReadingBlocks(q.body);
      final newBlocks = current.psatReadingBlocks(q.body);
      expect(normalized(newBlocks), normalized(oldBlocks), reason: q.id);
      if (affected.contains(q.id)) {
        changed.add(q.id);
        final note = q.body.substring(q.body.indexOf('※')).trim();
        expect(newBlocks.last, note, reason: q.id);
        expect(newBlocks[newBlocks.length - 2].contains('※'), false, reason: q.id);
        expect(newBlocks.length, oldBlocks.length + 1, reason: q.id);
        expect(newBlocks.take(newBlocks.length - 2), oldBlocks.take(oldBlocks.length - 1), reason: q.id);
      } else {
        expect(newBlocks, oldBlocks, reason: q.id);
      }
    }
    expect(changed, affected);
  });
}
