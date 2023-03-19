// don't change the source code, this is a very important file

import 'dart:async';
import 'dart:io';
import 'package:app_updater/app_updater.dart';
import 'package:flutter/material.dart';
import 'package:flutter_webview_pro/webview_flutter.dart';
import 'package:splash_screen_view/SplashScreenView.dart';
import 'package:url_launcher/url_launcher.dart';
import 'screens/screens.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'APP_NAME',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      debugShowCheckedModeBanner: false,
      home: Splash(),
    );
  }
}

// ignore: non_constant_identifier_names
Widget Splash() {
  return SplashScreenView(
    navigateRoute: const MyHomePage(),
    duration: 1000,
    imageSize: 130,
    imageSrc: "assets/images/favicon.png",
    backgroundColor: Colors.white,
  );
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({Key? key}) : super(key: key);
  @override
  _MyHomePageState createState() => _MyHomePageState();
}

WebViewController? controllerGlobal;
willPopScope() async {
  if (await controllerGlobal!.canGoBack()) {
    controllerGlobal!.goBack();
    return false;
  } else {
    return true;
  }
}

class _MyHomePageState extends State<MyHomePage> {
  bool loading = true;
  @override
  void initState() {
    super.initState();
    if (Platform.isAndroid) WebView.platform = SurfaceAndroidWebView();
    if (Platform.isIOS) WebView.platform = CupertinoWebView();
    checkAppUpdate(
      context,
      appName: 'APP_NAME',
      iosAppId: 'IOS_APP_ID',
      androidAppBundleId: 'ANDROID_PACKAGE_NAME',
    );
  }

  @override
  Widget build(BuildContext context) {
    final Completer<WebViewController> controllerCompleter =
        Completer<WebViewController>();

    String url = 'https://WEBSITE';
    return SafeArea(
      child: WillPopScope(
        onWillPop: () => willPopScope(),
        child: Scaffold(
          body: RefreshIndicator(
            onRefresh: () async {
              await controllerGlobal!.reload();
            },
            child: Builder(
              builder: (BuildContext context) {
                return Stack(
                  children: <Widget>[
                    SizedBox(
                      child: WebView(
                        initialUrl: url,
                        javascriptMode: JavascriptMode.unrestricted,
                        onWebResourceError: (WebResourceError error) {
                          Navigator.pushAndRemoveUntil(
                            context,
                            MaterialPageRoute(
                                builder: (context) => const ErrorPage()),
                            (Route<dynamic> route) => false,
                          );
                        },
                        onProgress: (int progress) {
                          const Center(child: CircularProgressIndicator());
                        },
                        onWebViewCreated:
                            (WebViewController webViewController) {
                          controllerCompleter.future
                              .then((value) => controllerGlobal = value);
                          controllerCompleter.complete(webViewController);
                        },
                        onPageStarted: ((url) {
                          setState(() {
                            loading = true;
                          });
                        }),
                        onPageFinished: ((url) {
                          setState(() {
                            loading = false;
                          });
                        }),
                        navigationDelegate: (NavigationRequest request) {
                          if (request.url.startsWith(url)) {
                            return NavigationDecision.navigate;
                          } else if (request.url.contains(url)) {
                            return NavigationDecision.navigate;
                          } else {
                            launchURL(request.url);
                            return NavigationDecision.prevent;
                          }
                        },
                        zoomEnabled: false,
                        gestureNavigationEnabled: true,
                        geolocationEnabled: true,
                      ),
                    ),
                    Positioned(
                      child: Visibility(
                        visible: loading,
                        child: const Center(
                          child: CircularProgressIndicator(),
                        ),
                      ),
                    ),
                  ],
                );
              },
            ),
          ),
        ),
      ),
    );
  }

  launchURL(String url) async {
    // ignore: deprecated_member_use
    if (await canLaunch(url)) {
      // ignore: deprecated_member_use
      await launch(url);
    } else {
      throw 'Could not launch $url';
    }
  }
}
