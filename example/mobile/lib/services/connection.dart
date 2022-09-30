import 'package:flutter/material.dart';
import 'package:internet_connection_checker/internet_connection_checker.dart';

Future<void> checkInternetConnection() async {
  bool result = await InternetConnectionChecker().hasConnection;
  if (result == true) {
    // ignore: avoid_print
    print('Online.');
  } else {
    // ignore: avoid_print
    print('Offline.');
    MaterialPageRoute(builder: (_) => noInternetPage());
  }
}

Widget noInternetPage() {
  return ListView(
    children: [
      Container(
        decoration: const BoxDecoration(color: Colors.blue),
      ),
    ],
  );
}
