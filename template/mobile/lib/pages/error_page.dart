import 'package:flutter/material.dart';
import 'package:flutter_bounceable/flutter_bounceable.dart';
import '../screens/screens.dart';

class ErrorPage extends StatefulWidget {
  const ErrorPage({Key? key}) : super(key: key);

  @override
  State<ErrorPage> createState() => _ErrorPageState();
}

class _ErrorPageState extends State<ErrorPage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        decoration: const BoxDecoration(
          color: Colors.white,
        ),
        child: Center(
          child: ListView(
            children: [
              const SizedBox(height: 200),
              const SizedBox(
                width: 300,
                height: 300,
                child: Image(
                  image: AssetImage('assets/images/error.png'),
                ),
              ),
              const SizedBox(height: 20),
              const Center(
                child: Text(
                  'Something went wrong',
                  style: TextStyle(
                    fontSize: 20,
                    fontWeight: FontWeight.w500,
                  ),
                ),
              ),
              const SizedBox(height: 20),
              Center(
                child: Bounceable(
                  onTap: () {
                    Navigator.pushAndRemoveUntil(
                      context,
                      MaterialPageRoute(
                          builder: (context) => const MyHomePage()),
                      (Route<dynamic> route) => false,
                    );
                  },
                  child: Container(
                    width: 100,
                    height: 30,
                    decoration: BoxDecoration(
                      color: Colors.white.withOpacity(0.3),
                      borderRadius: BorderRadius.circular(30),
                      border: Border.all(
                        color: Colors.black.withOpacity(0.6),
                        width: 1,
                      ),
                    ),
                    child: const Center(child: Text('Try Again')),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
