import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:grit/practice.dart';
import 'package:grit/model.dart';
import 'ui_test.dart' show sample;

void main() {
  for (final size in [const Size(360, 840), const Size(752, 834)]) {
    testWidgets('every result and review type stays usable at $size', (
      tester,
    ) async {
      tester.view.physicalSize = size;
      tester.view.devicePixelRatio = 1;
      addTearDown(tester.view.resetPhysicalSize);
      addTearDown(tester.view.resetDevicePixelRatio);
      for (final kind in SetKind.values) {
        final s = sample(kind)
          ..elapsedSeconds = 130
          ..completedAt = DateTime.now();
        await tester.pumpWidget(
          MaterialApp(
            home: ResultScreen(key: ValueKey(kind), session: s),
          ),
        );
        await tester.pumpAndSettle();
        final view = find
            .descendant(
              of: find.byType(ListView).first,
              matching: find.byType(Scrollable),
            )
            .first;
        await tester.scrollUntilVisible(
          find.text('돌아가기'),
          400,
          scrollable: view,
          maxScrolls: 100,
        );
        expect(tester.takeException(), isNull, reason: kind.name);
        expect(find.text('돌아가기').hitTestable(), findsOneWidget);
      }
      await tester.pumpWidget(const SizedBox());
    });
  }
}
