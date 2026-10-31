import 'dart:convert';
import 'package:flutter/services.dart';

class PsatQuestion {
  final Map<String, dynamic> data;
  PsatQuestion.fromJson(Map<String, dynamic> value)
    : data = Map<String, dynamic>.from(jsonDecode(jsonEncode(value)) as Map) {
    if (id.isEmpty ||
        !['자료해석', '언어논리', '상황판단'].contains(subject) ||
        choices.length != 5 ||
        answer < 1 ||
        answer > 5 ||
        reasons.length != 5 ||
        steps.isEmpty ||
        (body.isEmpty && figures.isEmpty) ||
        !original.startsWith('assets/psat/originals/')) {
      throw const FormatException('잘못된 PSAT 문항');
    }
    for (final key in [
      'title',
      'tag',
      'prompt',
      'source',
      'book',
      'sourceUrl',
      'answerUrl',
      'editNote',
      'pitfall',
      'transfer',
    ]) {
      if (data[key] is! String || (data[key] as String).trim().isEmpty) {
        throw const FormatException('누락된 PSAT 문항 정보');
      }
    }
    if (number < 1 ||
        [...choices, ...steps, ...reasons].any((x) => x.trim().isEmpty)) {
      throw const FormatException('빈 PSAT 문항 내용');
    }
    final markedRanges = <(int, int)>[];
    for (final phrase in underlines) {
      final matches = phrase.isEmpty
          ? <RegExpMatch>[]
          : RegExp(RegExp.escape(phrase)).allMatches(body).toList();
      if (matches.length != 1 || phrase.contains('\n')) {
        throw const FormatException('잘못된 원문 밑줄 범위');
      }
      final match = matches.single;
      if (markedRanges.any((r) => match.start < r.$2 && match.end > r.$1)) {
        throw const FormatException('중복된 원문 밑줄 범위');
      }
      markedRanges.add((match.start, match.end));
    }
    for (final figure in figures) {
      if (figure['asset'] is! String ||
          !(figure['asset'] as String).startsWith('assets/psat/figures/') ||
          figure['caption'] is! String ||
          (figure['caption'] as String).isEmpty ||
          figure['width'] is! num ||
          figure['height'] is! num ||
          (figure['width'] as num) <= 0 ||
          (figure['height'] as num) <= 0) {
        throw const FormatException('잘못된 자료 이미지');
      }
    }
    for (final table in tables) {
      final after = table['afterParagraph'];
      if (after != null &&
          (after is! int ||
              after < 0 ||
              after >= body.split(RegExp(r'\n\s*\n')).length)) {
        throw const FormatException('잘못된 표의 본문 위치');
      }
      final cols = List<String>.from(table['columns'] as List);
      if (cols.length < 2 || table['caption'] is! String) {
        throw const FormatException('잘못된 표');
      }
      for (final row in table['rows'] as List) {
        if (List<String>.from(row as List).length != cols.length) {
          throw const FormatException('잘못된 표의 행');
        }
      }
    }
  }
  String get id => data['id'] as String;
  String get subject => data['subject'] as String;
  String get title => data['title'] as String;
  String get tag => data['tag'] as String;
  String get body => data['body'] as String;
  String get prompt => data['prompt'] as String;
  String get original => data['original'] as String;
  int get number => data['number'] as int;
  int get answer => data['answer'] as int;
  List<String> get underlines =>
      List<String>.from(data['underlines'] as List? ?? const []);
  List<String> get choices => List<String>.from(data['choices'] as List);
  List<String> get steps => List<String>.from(data['steps'] as List);
  List<String> get reasons => List<String>.from(data['optionReasons'] as List);
  List<Map<String, dynamic>> get tables => (data['tables'] as List)
      .map((x) => Map<String, dynamic>.from(x as Map))
      .toList();
  List<Map<String, dynamic>> get figures => (data['figures'] as List? ?? [])
      .map((x) => Map<String, dynamic>.from(x as Map))
      .toList();
  Map<String, dynamic> toJson() =>
      jsonDecode(jsonEncode(data)) as Map<String, dynamic>;
}

Future<List<PsatQuestion>> loadPsatBank() async {
  final raw = <dynamic>[];
  for (final asset in [
    'assets/psat/batch01.json',
    'assets/psat/data01.json',
    'assets/psat/verbal02.json',
    'assets/psat/situation02.json',
    'assets/psat/data02.json',
    'assets/psat/verbal03.json',
    'assets/psat/situation03.json',
    'assets/psat/data03.json',
    'assets/psat/verbal04.json',
    'assets/psat/situation04.json',
    'assets/psat/data04.json',
    'assets/psat/verbal05.json',
    'assets/psat/situation05.json',
    'assets/psat/data05.json',
    'assets/psat/verbal06.json',
    'assets/psat/situation06.json',
    'assets/psat/data06.json',
    'assets/psat/verbal07.json',
    'assets/psat/situation07.json',
    'assets/psat/data07.json',
    'assets/psat/verbal08.json',
    'assets/psat/situation08.json',
    'assets/psat/data08.json',
    'assets/psat/verbal09.json',
    'assets/psat/situation09.json',
    'assets/psat/data09.json',
    'assets/psat/verbal10.json',
    'assets/psat/situation10.json',
    'assets/psat/data10.json',
    'assets/psat/verbal11.json',
    'assets/psat/situation11.json',
    'assets/psat/data11.json',
    'assets/psat/verbal12.json',
    'assets/psat/situation12.json',
    'assets/psat/data12.json',
    'assets/psat/verbal13.json',
    'assets/psat/situation13.json',
    'assets/psat/data13.json',
    'assets/psat/verbal14.json',
    'assets/psat/situation14.json',
    'assets/psat/data14.json',
    'assets/psat/verbal15.json',
    'assets/psat/situation15.json',
    'assets/psat/data15.json',
    'assets/psat/verbal16.json',
    'assets/psat/situation16.json',
    'assets/psat/data16.json',
    'assets/psat/verbal17.json',
    'assets/psat/situation17.json',
    'assets/psat/data17.json',
    'assets/psat/verbal18.json',
    'assets/psat/situation18.json',
    'assets/psat/data18.json',
    'assets/psat/verbal19.json',
    'assets/psat/situation19.json',
    'assets/psat/data19.json',
    'assets/psat/verbal20.json',
    'assets/psat/verbal21.json',
    'assets/psat/verbal22.json',
    'assets/psat/verbal23.json',
    'assets/psat/verbal24.json',
    'assets/psat/verbal25.json',
    'assets/psat/verbal26.json',
    'assets/psat/verbal27.json',
    'assets/psat/verbal28.json',
    'assets/psat/verbal29.json',
    'assets/psat/situation20.json',
    'assets/psat/situation21.json',
    'assets/psat/situation22.json',
    'assets/psat/situation23.json',
    'assets/psat/situation24.json',
    'assets/psat/situation25.json',
    'assets/psat/situation26.json',
    'assets/psat/situation27.json',
    'assets/psat/situation28.json',
    'assets/psat/situation29.json',
    'assets/psat/data20.json',
    'assets/psat/data21.json',
    'assets/psat/data22.json',
    'assets/psat/data23.json',
    'assets/psat/data24.json',
    'assets/psat/data25.json',
    'assets/psat/data26.json',
    'assets/psat/data27.json',
    'assets/psat/data28.json',
    'assets/psat/data29.json',
    'assets/psat/data30.json',
    'assets/psat/verbal30.json',
    'assets/psat/situation30.json',
  ]) {
    raw.addAll(jsonDecode(await rootBundle.loadString(asset)) as List);
  }
  final questions = raw
      .map((x) => PsatQuestion.fromJson(Map<String, dynamic>.from(x as Map)))
      .toList();
  if (questions.map((q) => q.id).toSet().length != questions.length) {
    throw const FormatException('중복된 PSAT 문항');
  }
  return questions;
}

class PsatAttempt {
  final String id;
  final PsatQuestion question;
  final int selected;
  final DateTime startedAt;
  final DateTime completedAt;
  final int seconds;
  PsatAttempt({
    required this.id,
    required this.question,
    required this.selected,
    required this.startedAt,
    required this.completedAt,
    required this.seconds,
  }) {
    if (selected < 1 ||
        selected > 5 ||
        seconds < 0 ||
        completedAt.isBefore(startedAt)) {
      throw const FormatException('잘못된 PSAT 풀이 기록');
    }
  }
  bool get correct => selected == question.answer;
  Map<String, dynamic> toJson() => {
    'id': id,
    'question': question.toJson(),
    'selected': selected,
    'startedAt': startedAt.toIso8601String(),
    'completedAt': completedAt.toIso8601String(),
    'seconds': seconds,
  };
  factory PsatAttempt.fromJson(Map<String, dynamic> x) => PsatAttempt(
    id: x['id'] as String,
    question: PsatQuestion.fromJson(
      Map<String, dynamic>.from(x['question'] as Map),
    ),
    selected: x['selected'] as int,
    startedAt: DateTime.parse(x['startedAt'] as String),
    completedAt: DateTime.parse(x['completedAt'] as String),
    seconds: x['seconds'] as int,
  );
}
