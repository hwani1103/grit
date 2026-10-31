import 'dart:ui' show DisplayFeatureType;
import 'package:flutter/material.dart';

/// Keep confirmation dialogs centered on a continuous folding display.
/// A physical hinge/cutout still reserves its normal safe region.
Future<T?> showGritDialog<T>({
  required BuildContext context,
  required WidgetBuilder builder,
}) {
  final navigator = Navigator.of(context, rootNavigator: true);
  return navigator.push<T>(
    _GritDialogRoute<T>(
      context: context,
      builder: builder,
      themes: InheritedTheme.capture(from: context, to: navigator.context),
      barrierColor:
          DialogTheme.of(context).barrierColor ??
          Theme.of(context).dialogTheme.barrierColor ??
          Colors.black54,
    ),
  );
}

class _GritDialogRoute<T> extends DialogRoute<T> {
  _GritDialogRoute({
    required super.context,
    required super.builder,
    required super.themes,
    required super.barrierColor,
  }) : super(traversalEdgeBehavior: TraversalEdgeBehavior.closedLoop);

  @override
  Widget buildPage(
    BuildContext context,
    Animation<double> animation,
    Animation<double> secondaryAnimation,
  ) {
    final media = MediaQuery.of(context);
    return MediaQuery(
      data: media.copyWith(
        displayFeatures: media.displayFeatures
            .where(
              (feature) =>
                  feature.type != DisplayFeatureType.fold ||
                  feature.bounds.shortestSide > 0,
            )
            .toList(),
      ),
      // Must wrap the route's DisplayFeatureSubScreen, not only AlertDialog.
      child: super.buildPage(context, animation, secondaryAnimation),
    );
  }
}
