import 'dart:math';

enum SetKind { addition, multiplication, division }

extension SetKindInfo on SetKind {
  String get title => switch (this) {
    SetKind.addition => '덧셈·뺄셈',
    SetKind.multiplication => '곱셈',
    SetKind.division => '나눗셈',
  };
  String get subtitle => switch (this) {
    SetKind.addition => '합계를 따라, 빈칸을 채우는 연습',
    SetKind.multiplication => '끝까지 계산하지 않고 크기를 읽는 연습',
    SetKind.division => '비슷한 비율 사이의 차이를 발견하는 연습',
  };
  String get quantity => switch (this) {
    SetKind.addition => '표 5개 · 답칸 40개',
    SetKind.multiplication => '곱 비교 8개 · 분수 비교 10개',
    SetKind.division => '분수 정렬 5개 · 분수 비교 10개',
  };
}

enum ProblemType { table, product, fraction, order }

class Problem {
  final ProblemType type;
  final List<List<int>> values;
  final List<int> hidden;
  const Problem(this.type, this.values, [this.hidden = const []]);
  int get width => values.first.length;
  int get total => type == ProblemType.table ? hidden.length : 1;
  String answerKey(int index, [int? cell]) =>
      '$index${cell == null ? '' : ':$cell'}';
  String get relation {
    final a = values[0], b = values[1];
    final left = type == ProblemType.product ? a[0] * a[1] : a[0] * b[1];
    final right = type == ProblemType.product ? b[0] * b[1] : b[0] * a[1];
    return left > right ? '>' : '<';
  }

  List<int> get ordered => List.generate(4, (i) => i)
    ..sort(
      (a, b) =>
          (values[b][0] * values[a][1]).compareTo(values[a][0] * values[b][1]),
    );
  Map<String, String> expected(int index) {
    if (type == ProblemType.table) {
      return {
        for (final cell in hidden)
          answerKey(index, cell): '${values[cell ~/ width][cell % width]}',
      };
    }
    return {
      answerKey(index): type == ProblemType.order
          ? ordered.join(',')
          : relation,
    };
  }

  Map<String, Object> toJson() => {
    'type': type.name,
    'values': values,
    'hidden': hidden,
  };
  factory Problem.fromJson(Map<String, dynamic> json) {
    final type = ProblemType.values.byName(json['type'] as String);
    final values = (json['values'] as List)
        .map((r) => (r as List).cast<int>().toList())
        .toList();
    final hidden = (json['hidden'] as List).cast<int>().toList();
    if (values.isEmpty ||
        values.length > 6 ||
        values.any(
          (r) => r.isEmpty || r.length > 7 || r.any((v) => v.abs() > 1000000),
        )) {
      throw const FormatException('잘못된 문제 형식');
    }
    if (type == ProblemType.table) {
      if (values.any((r) => r.length != values.first.length) ||
          hidden.toSet().length != hidden.length ||
          hidden.any(
            (i) => i < 0 || i >= values.length * values.first.length,
          )) {
        throw const FormatException('잘못된 표');
      }
    } else if (values.length != (type == ProblemType.order ? 4 : 2) ||
        values.any((r) => r.length != 2 || r.any((v) => v <= 0))) {
      throw const FormatException('잘못된 비교 문제');
    }
    return Problem(type, values, hidden);
  }
}

class PracticeSession {
  final String id;
  final SetKind kind;
  final int seed;
  final List<Problem> problems;
  final DateTime startedAt;
  DateTime? completedAt;
  int? elapsedSeconds;
  // Unfinished sessions live only in memory. Keep subsecond background time
  // here so repeated app switches do not add rounding errors to saved results.
  Duration _backgroundTime = Duration.zero;
  DateTime? _backgroundSince;
  final Map<String, String> answers;
  final Map<String, String> memos;
  int page;
  PracticeSession({
    required this.id,
    required this.kind,
    required this.seed,
    required this.problems,
    required this.startedAt,
    this.completedAt,
    this.elapsedSeconds,
    Map<String, String>? answers,
    Map<String, String>? memos,
    this.page = 0,
  }) : answers = answers ?? {},
       memos = memos ?? {};
  Set<String> get memoKeys => {
    for (var i = 0; i < problems.length; i++)
      if (problems[i].type == ProblemType.table) ...{
        for (var r = 0; r < problems[i].values.length; r++) '$i:r:$r',
        for (var c = 0; c < problems[i].width; c++) '$i:c:$c',
      },
  };
  int get total => problems.fold(0, (a, p) => a + p.total);
  Map<String, String> get expected => {
    for (var i = 0; i < problems.length; i++) ...problems[i].expected(i),
  };
  bool matches(String key, String expectedValue) {
    final answer = answers[key]?.trim();
    if (key.contains(':')) {
      return int.tryParse(answer ?? '') == int.tryParse(expectedValue);
    }
    return answer == expectedValue;
  }

  int get correct =>
      expected.entries.where((e) => matches(e.key, e.value)).length;
  bool hasAnswer(String key) {
    final answer = answers[key]?.trim() ?? '';
    if (key.contains(':')) return int.tryParse(answer) != null;
    final index = int.parse(key);
    return problems[index].type == ProblemType.order
        ? answer.split(',').length == 4
        : answer == '<' || answer == '>';
  }

  int get answered => expected.keys.where(hasAnswer).length;
  bool get isTimingPaused => _backgroundSince != null;
  void pauseTiming(DateTime now) {
    if (completedAt == null) _backgroundSince ??= now;
  }

  void resumeTiming(DateTime now) {
    final since = _backgroundSince;
    if (since == null) return;
    if (now.isAfter(since)) _backgroundTime += now.difference(since);
    _backgroundSince = null;
  }

  int elapsedAt(DateTime now) {
    if (elapsedSeconds != null) return elapsedSeconds!;
    final since = _backgroundSince;
    final end = since != null && since.isBefore(now) ? since : now;
    return max(0, (end.difference(startedAt) - _backgroundTime).inSeconds);
  }

  Map<String, dynamic> toJson() => {
    'id': id,
    'kind': kind.name,
    'seed': seed,
    'generatorVersion': 1,
    'problems': problems.map((p) => p.toJson()).toList(),
    'startedAt': startedAt.toIso8601String(),
    'completedAt': completedAt?.toIso8601String(),
    'elapsedSeconds': elapsedSeconds,
    'answers': answers,
    'memos': memos,
    'page': page,
  };
  factory PracticeSession.fromJson(Map<String, dynamic> j) {
    if (j['generatorVersion'] != 1) {
      throw const FormatException('지원하지 않는 문제 버전');
    }
    final kind = SetKind.values.byName(j['kind'] as String);
    final problems = (j['problems'] as List)
        .map((p) => Problem.fromJson(Map<String, dynamic>.from(p as Map)))
        .toList();
    final count = switch (kind) {
      SetKind.addition => 5,
      SetKind.multiplication => 18,
      SetKind.division => 15,
    };
    if (problems.length != count) throw const FormatException('문제 수가 맞지 않음');
    for (var i = 0; i < count; i++) {
      final p = problems[i];
      final wanted = switch (kind) {
        SetKind.addition => ProblemType.table,
        SetKind.multiplication =>
          i < 8 ? ProblemType.product : ProblemType.fraction,
        SetKind.division => i < 5 ? ProblemType.order : ProblemType.fraction,
      };
      if (p.type != wanted) throw const FormatException('문제 유형이 맞지 않음');
      if (wanted == ProblemType.table) {
        final spec = Generator.tableSpecs[i];
        if (p.values.length != spec[0] + 1 ||
            p.width != spec[1] + 1 ||
            p.hidden.length != spec[2] ||
            Generator.solveRounds(p) == 0) {
          throw const FormatException('표 조건이 맞지 않음');
        }
        final r = p.values.length - 1, c = p.width - 1;
        for (var y = 0; y <= r; y++) {
          if (p.values[y].take(c).fold(0, (a, b) => a + b) != p.values[y][c]) {
            throw const FormatException('표 합계 오류');
          }
        }
        for (var x = 0; x <= c; x++) {
          if (p.values.take(r).fold(0, (a, row) => a + row[x]) !=
              p.values[r][x]) {
            throw const FormatException('표 합계 오류');
          }
        }
      } else {
        final sorted = p.type == ProblemType.order ? p.ordered : [0, 1];
        for (var k = 1; k < sorted.length; k++) {
          final a = p.values[sorted[k - 1]], b = p.values[sorted[k]];
          if (p.type == ProblemType.product
              ? a[0] * a[1] == b[0] * b[1]
              : a[0] * b[1] == b[0] * a[1]) {
            throw const FormatException('같은 값 비교');
          }
        }
      }
    }
    final answers = Map<String, String>.from(j['answers'] as Map);
    final completed = j['completedAt'] == null
        ? null
        : DateTime.parse(j['completedAt'] as String);
    final elapsed = j['elapsedSeconds'] as int?;
    if ((completed == null) != (elapsed == null) ||
        (elapsed != null && elapsed < 0)) {
      throw const FormatException('잘못된 시간 기록');
    }
    final session = PracticeSession(
      id: j['id'] as String,
      kind: kind,
      seed: j['seed'] as int,
      problems: problems,
      startedAt: DateTime.parse(j['startedAt'] as String),
      completedAt: completed,
      elapsedSeconds: elapsed,
      answers: answers,
      memos: j.containsKey('memos')
          ? Map<String, String>.from(j['memos'] as Map)
          : {},
      page: (j['page'] as int).clamp(0, count - 1),
    );
    if (answers.keys.any((key) => !session.expected.containsKey(key)) ||
        answers.values.any((v) => v.length > 32)) {
      throw const FormatException('잘못된 답안');
    }
    for (final entry in answers.entries) {
      if (!entry.key.contains(':') &&
          problems[int.parse(entry.key)].type == ProblemType.order &&
          entry.value.isNotEmpty) {
        final indices = entry.value.split(',').map(int.tryParse).toList();
        if (indices.any((i) => i == null || i < 0 || i > 3) ||
            indices.toSet().length != indices.length) {
          throw const FormatException('잘못된 정렬 답안');
        }
      }
    }
    if (session.memos.keys.any((key) => !session.memoKeys.contains(key)) ||
        session.memos.values.any((v) => !RegExp(r'^-?\d{0,6}$').hasMatch(v))) {
      throw const FormatException('잘못된 계산 메모');
    }
    return session;
  }
}

class Generator {
  final Random random;
  Generator(int seed) : random = Random(seed);
  int between(int low, int high) => low + random.nextInt(high - low + 1);
  static const tableSpecs = [
    [3, 3, 7, 10, 99],
    [4, 4, 8, 0, 59],
    [3, 3, 7, -50, 49],
    [4, 4, 8, -30, 29],
    [5, 6, 10, -10, 29],
  ];
  List<Problem> generate(SetKind kind) {
    final result = <Problem>[];
    final signatures = <String>{};
    final count = switch (kind) {
      SetKind.addition => 5,
      SetKind.multiplication => 18,
      SetKind.division => 15,
    };
    for (var i = 0; i < count; i++) {
      Problem p;
      String signature;
      do {
        p = switch (kind) {
          SetKind.addition => table(i),
          SetKind.multiplication => i < 8 ? product() : fraction(),
          SetKind.division => i < 5 ? order(i < 3 ? 349 : 999) : fraction(),
        };
        final parts = p.values.map((r) => r.join('/')).toList()..sort();
        signature =
            p.type.name +
            parts.join('|') +
            (p.type == ProblemType.table ? p.hidden.join(',') : '');
      } while (!signatures.add(signature));
      result.add(p);
    }
    return result;
  }

  Problem table(int index) {
    final s = tableSpecs[index], rows = s[0], cols = s[1];
    List<List<int>> grid;
    do {
      grid = List.generate(rows + 1, (_) => List.filled(cols + 1, 0));
      for (var r = 0; r < rows; r++) {
        for (var c = 0; c < cols; c++) {
          final value = between(s[3], s[4]);
          grid[r][c] = value;
          grid[r][cols] += value;
          grid[rows][c] += value;
          grid[rows][cols] += value;
        }
      }
    } while (index >= 2 &&
        (!grid.take(rows).any((r) => r.take(cols).any((x) => x < 0)) ||
            !grid.take(rows).any((r) => r.take(cols).any((x) => x > 0))));
    for (var attempt = 0; attempt < 20000; attempt++) {
      final cells = List.generate((rows + 1) * (cols + 1), (i) => i)
        ..shuffle(random);
      final hidden = cells.take(s[2]).toList()..sort();
      final problem = Problem(ProblemType.table, grid, hidden);
      final rounds = solveRounds(problem);
      if (rounds >= 2 && rounds <= 4) return problem;
    }
    throw StateError('표 생성 조건을 만족하지 못했습니다. 다시 시작해 주세요.');
  }

  static int solveRounds(Problem p) {
    final r = p.values.length - 1, c = p.width - 1;
    final remaining = p.hidden.toSet();
    var rounds = 0;
    while (remaining.isNotEmpty) {
      final found = <int>{};
      for (var y = 0; y <= r; y++) {
        final cells = List.generate(
          c + 1,
          (x) => y * (c + 1) + x,
        ).where(remaining.contains).toList();
        if (cells.length == 1) found.add(cells.single);
      }
      for (var x = 0; x <= c; x++) {
        final cells = List.generate(
          r + 1,
          (y) => y * (c + 1) + x,
        ).where(remaining.contains).toList();
        if (cells.length == 1) found.add(cells.single);
      }
      if (found.isEmpty) return 0;
      remaining.removeAll(found);
      rounds++;
    }
    return rounds;
  }

  static double gap(int a, int b) => (a - b).abs() / max(a, b);
  Problem product() {
    for (var attempt = 0; attempt < 100000; attempt++) {
      final a = between(1000, 10099),
          b = between(10, 999),
          c = between(1000, 10099),
          d = between(10, 999);
      if ((a - c) * (b - d) >= 0) continue;
      final g = gap(a * b, c * d);
      if (g >= .10 && g <= .25) {
        return Problem(ProblemType.product, [
          [a, b],
          [c, d],
        ]);
      }
    }
    throw StateError('곱 비교 생성 실패');
  }

  Problem fraction() {
    final bucket = random.nextInt(100);
    final low = bucket < 12
        ? 0.0
        : bucket < 44
        ? .01
        : bucket < 74
        ? .05
        : .10;
    final high = bucket < 12
        ? .01
        : bucket < 44
        ? .05
        : bucket < 74
        ? .10
        : .14;
    for (var attempt = 0; attempt < 100000; attempt++) {
      final a = between(10, 349), b = between(10, 349), d = between(10, 349);
      final target = low + random.nextDouble() * (high - low);
      final ratio =
          (a / b) * (random.nextBool() ? 1 - target : 1 / (1 - target));
      final c = (ratio * d).round();
      if (c < 10 || c > 349 || a * d == c * b) continue;
      final g = gap(a * d, c * b);
      if (g >= low && g < high) {
        final pair = [
          [a, b],
          [c, d],
        ];
        if (random.nextBool()) {
          return Problem(ProblemType.fraction, pair.reversed.toList());
        }
        return Problem(ProblemType.fraction, pair);
      }
    }
    throw StateError('분수 비교 생성 실패');
  }

  Problem order(int maximum) {
    for (var attempt = 0; attempt < 100000; attempt++) {
      var ratio = .35 + random.nextDouble() * 1.15;
      final pairs = <List<int>>[];
      for (var i = 0; i < 4; i++) {
        if (i > 0) ratio /= 1 - (.035 + random.nextDouble() * .105);
        final lowD = max(10, (10 / ratio).ceil());
        final highD = min(maximum, (maximum / ratio).floor());
        if (lowD > highD) break;
        final d = between(lowD, highD), n = (ratio * d).round();
        pairs.add([n, d]);
      }
      if (pairs.length != 4 ||
          pairs.any(
            (p) =>
                p[0] < 10 ||
                p[0] > maximum ||
                p[0] / p[1] < .35 ||
                p[0] / p[1] > 2,
          )) {
        continue;
      }
      pairs.sort((a, b) => (a[0] * b[1]).compareTo(b[0] * a[1]));
      final spread = gap(
        pairs.first[0] * pairs.last[1],
        pairs.last[0] * pairs.first[1],
      );
      if (spread < .17 || spread > .28) continue;
      var valid = true;
      for (var i = 1; i < 4; i++) {
        final g = gap(
          pairs[i - 1][0] * pairs[i][1],
          pairs[i][0] * pairs[i - 1][1],
        );
        if (g < .035 || g > .14) valid = false;
      }
      if (valid) {
        pairs.shuffle(random);
        return Problem(ProblemType.order, pairs);
      }
    }
    throw StateError('정렬 문제 생성 실패');
  }
}

String durationLabel(int seconds) {
  final minutes = seconds ~/ 60;
  return '$minutes분 ${(seconds % 60).toString().padLeft(2, '0')}초';
}

String clockLabel(int seconds) =>
    '${seconds ~/ 60}:${(seconds % 60).toString().padLeft(2, '0')}';
String dateLabel(DateTime date) =>
    '${date.year}.${'${date.month}'.padLeft(2, '0')}.${'${date.day}'.padLeft(2, '0')}';
