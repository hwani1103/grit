import 'dart:convert';
import 'package:flutter/services.dart';
import 'psat_model.dart';

class PsatSet {
  final String id;
  final String subject;
  final int order;
  final String difficulty;
  final List<String> questionIds;
  PsatSet.fromJson(Map<String, dynamic> json)
    : id = json['id'] as String,
      subject = json['subject'] as String,
      order = json['order'] as int,
      difficulty = json['difficulty'] as String? ?? '혼합',
      questionIds = List<String>.unmodifiable(json['questionIds'] as List) {
    if (id.trim().isEmpty ||
        !['자료해석', '언어논리', '상황판단'].contains(subject) ||
        order < 1 ||
        !['기본', '심화', '고난도', '혼합'].contains(difficulty) ||
        questionIds.length != 10 ||
        questionIds.toSet().length != 10 ||
        questionIds.any((id) => id.trim().isEmpty)) {
      throw const FormatException('잘못된 PSAT Set');
    }
  }
  String get title => 'Set $order';
}

class PsatCatalog {
  final Map<String, PsatQuestion> questions;
  final List<PsatSet> sets;
  PsatCatalog(List<PsatQuestion> bank, Map<String, dynamic> manifest)
    : questions = Map.unmodifiable({for (final q in bank) q.id: q}),
      sets = List.unmodifiable(
        (manifest['sets'] as List).map(
          (s) => PsatSet.fromJson(Map<String, dynamic>.from(s as Map)),
        ),
      ) {
    if (manifest['schemaVersion'] != 1 || questions.length != bank.length) {
      throw const FormatException('잘못된 PSAT 목록');
    }
    final setIds = <String>{};
    final orders = <String>{};
    final assigned = <String>{};
    for (final set in sets) {
      if (!setIds.add(set.id) || !orders.add('${set.subject}:${set.order}')) {
        throw const FormatException('중복된 PSAT Set');
      }
      for (final id in set.questionIds) {
        if (!assigned.add(id) || questions[id]?.subject != set.subject) {
          throw const FormatException('PSAT Set 문항 연결 오류');
        }
      }
    }
    if (assigned.length != questions.length) {
      throw const FormatException('Set에 배정되지 않은 PSAT 문항');
    }
  }
  List<PsatSet> forSubject(String subject) =>
      sets.where((s) => s.subject == subject).toList()
        ..sort((a, b) => a.order.compareTo(b.order));
}

Future<PsatCatalog> loadPsatCatalog() async {
  final bank = await loadPsatBank();
  final manifest =
      jsonDecode(await rootBundle.loadString('assets/psat/sets.json'))
          as Map<String, dynamic>;
  return PsatCatalog(bank, manifest);
}

// Only committed records contribute. No separate progress counter can drift.
class PsatProgress {
  final Map<String, PsatAttempt> latest;
  PsatProgress(Iterable<PsatAttempt> records) : latest = {} {
    for (final attempt in records) {
      final previous = latest[attempt.question.id];
      if (previous == null ||
          attempt.completedAt.isAfter(previous.completedAt)) {
        latest[attempt.question.id] = attempt;
      }
    }
  }
  int completed(PsatSet set) =>
      set.questionIds.where(latest.containsKey).length;
  int wrong(PsatSet set) =>
      set.questionIds.where((id) => latest[id]?.correct == false).length;
}
