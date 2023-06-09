import 'package:flutter/material.dart';
import 'package:swab/pages/pages.dart';
import 'package:url_strategy/url_strategy.dart';

void main() {
  setPathUrlStrategy();
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        fontFamily: 'Poppins',
        primaryColor: const Color(0xFF1E1E1E),
        scaffoldBackgroundColor: const Color(0xFF1E1E1E),
      ),
      home: Scaffold(
        body: MediaQuery.of(context).size.width < 800
            ? const NotSupported()
            : const Home(),
      ),
    );
  }
}
