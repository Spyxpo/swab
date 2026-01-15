import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_inappwebview/flutter_inappwebview.dart';
import 'package:url_launcher/url_launcher.dart';
import 'package:connectivity_plus/connectivity_plus.dart';
import 'package:share_plus/share_plus.dart' as share_plus;

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  SystemChrome.setPreferredOrientations([
    DeviceOrientation.portraitUp,
    DeviceOrientation.portraitDown,
    DeviceOrientation.landscapeLeft,
    DeviceOrientation.landscapeRight,
  ]);
  runApp(const MyApp());
}

/// ================= Clipboard Channel (ADDED) =================
class ClipboardChannel {
  static const MethodChannel _channel =
      MethodChannel('swab/clipboard');

  static Future<void> copyText(String text) async {
    await _channel.invokeMethod('copyText', {
      'text': text,
    });
  }

  static Future<String> pasteText() async {
    final text = await _channel.invokeMethod<String>('pasteText');
    return text ?? '';
  }
}
/// ============================================================

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: '{{APP_NAME}}',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.blue),
        useMaterial3: true,
      ),
      darkTheme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
          seedColor: Colors.blue,
          brightness: Brightness.dark,
        ),
        useMaterial3: true,
      ),
      themeMode: ThemeMode.system,
      home: const WebViewScreen(),
    );
  }
}

class WebViewScreen extends StatefulWidget {
  const WebViewScreen({super.key});

  @override
  State<WebViewScreen> createState() => _WebViewScreenState();
}

class _WebViewScreenState extends State<WebViewScreen> {
  InAppWebViewController? webViewController;
  PullToRefreshController? pullToRefreshController;
  double progress = 0;
  String url = '{{APP_URL}}';
  bool isLoading = true;
  bool isOffline = false;
  bool canGoBack = false;
  bool canGoForward = false;

  static const bool ALLOW_ZOOM = true;
  static const bool ENABLE_JAVASCRIPT = true;
  static const bool ENABLE_DOM_STORAGE = true;
  static const bool ENABLE_GEOLOCATION = true;
  static const bool ENABLE_PULL_TO_REFRESH = true;
  static const bool SHOW_NAVIGATION_BAR = true;
  static const bool ENABLE_FILE_ACCESS = true;
  static const bool ENABLE_CACHE = true;
  static const bool ENABLE_MEDIA_AUTOPLAY = false;

  @override
  void initState() {
    super.initState();
    _checkConnectivity();
    pullToRefreshController = ENABLE_PULL_TO_REFRESH
        ? PullToRefreshController(
            settings: PullToRefreshSettings(color: Colors.blue),
            onRefresh: () async {
              webViewController?.reload();
            },
          )
        : null;
  }

  Future<void> _checkConnectivity() async {
    final connectivityResult = await Connectivity().checkConnectivity();
    setState(() {
      isOffline = connectivityResult.contains(ConnectivityResult.none);
    });

    Connectivity().onConnectivityChanged.listen((result) {
      setState(() {
        isOffline = result.contains(ConnectivityResult.none);
      });
      if (!isOffline) {
        webViewController?.reload();
      }
    });
  }

  Future<void> _updateNavigationState() async {
    final canBack = await webViewController?.canGoBack() ?? false;
    final canForward = await webViewController?.canGoForward() ?? false;
    setState(() {
      canGoBack = canBack;
      canGoForward = canForward;
    });
  }

  @override
  Widget build(BuildContext context) {
    return PopScope(
      canPop: !canGoBack,
      onPopInvokedWithResult: (didPop, result) async {
        if (!didPop && canGoBack) {
          webViewController?.goBack();
        }
      },
      child: Scaffold(
        body: SafeArea(
          child: Stack(
            children: [
              if (isOffline)
                _buildOfflineWidget()
              else
                InAppWebView(
                  initialUrlRequest: URLRequest(url: WebUri(url)),
                  initialSettings: InAppWebViewSettings(
                    useShouldOverrideUrlLoading: true,
                    mediaPlaybackRequiresUserGesture: !ENABLE_MEDIA_AUTOPLAY,
                    javaScriptEnabled: ENABLE_JAVASCRIPT,
                    domStorageEnabled: ENABLE_DOM_STORAGE,
                    databaseEnabled: ENABLE_DOM_STORAGE,
                    clearCache: !ENABLE_CACHE,
                    cacheEnabled: ENABLE_CACHE,
                    supportZoom: ALLOW_ZOOM,
                    allowFileAccess: ENABLE_FILE_ACCESS,
                    allowContentAccess: ENABLE_FILE_ACCESS,
                    geolocationEnabled: ENABLE_GEOLOCATION,
                    useHybridComposition: true,
                  ),
                  pullToRefreshController: pullToRefreshController,
                  onWebViewCreated: (controller) {
                    webViewController = controller;

                    /// ===== Clipboard JS Bridge (ADDED) =====
                    controller.addJavaScriptHandler(
                      handlerName: 'clipboard',
                      callback: (args) async {
                        final action = args[0];

                        if (action == 'copy') {
                          final text = args[1] as String;
                          await ClipboardChannel.copyText(text);
                          return true;
                        }

                        if (action == 'paste') {
                          final text = await ClipboardChannel.pasteText();
                          return text;
                        }

                        return null;
                      },
                    );
                    /// ======================================
                  },
                  onLoadStart: (controller, url) {
                    setState(() {
                      isLoading = true;
                    });
                  },
                  onLoadStop: (controller, url) async {
                    pullToRefreshController?.endRefreshing();
                    setState(() {
                      isLoading = false;
                    });
                    await _updateNavigationState();
                  },
                  onProgressChanged: (controller, progress) {
                    if (progress == 100) {
                      pullToRefreshController?.endRefreshing();
                    }
                    setState(() {
                      this.progress = progress / 100;
                      isLoading = progress < 100;
                    });
                  },
                  onReceivedError: (controller, request, error) {
                    pullToRefreshController?.endRefreshing();
                  },
                  shouldOverrideUrlLoading:
                      (controller, navigationAction) async {
                        final uri = navigationAction.request.url;
                        if (uri != null) {
                          final urlString = uri.toString();
                          if (!urlString.startsWith('http://') &&
                              !urlString.startsWith('https://')) {
                            if (await canLaunchUrl(uri)) {
                              await launchUrl(
                                uri,
                                mode: LaunchMode.externalApplication,
                              );
                              return NavigationActionPolicy.CANCEL;
                            }
                          }
                        }
                        return NavigationActionPolicy.ALLOW;
                      },
                  onDownloadStartRequest:
                      (controller, downloadStartRequest) async {
                        final downloadUrl = downloadStartRequest.url.toString();
                        if (await canLaunchUrl(Uri.parse(downloadUrl))) {
                          await launchUrl(
                            Uri.parse(downloadUrl),
                            mode: LaunchMode.externalApplication,
                          );
                        }
                      },
                ),
              if (isLoading && !isOffline)
                Positioned(
                  top: 0,
                  left: 0,
                  right: 0,
                  child: LinearProgressIndicator(
                    value: progress,
                    backgroundColor: Colors.grey[200],
                    valueColor: const AlwaysStoppedAnimation<Color>(
                      Colors.blue,
                    ),
                  ),
                ),
            ],
          ),
        ),
        bottomNavigationBar: !SHOW_NAVIGATION_BAR || isOffline
            ? null
            : Container(
                decoration: BoxDecoration(
                  color: Theme.of(context).scaffoldBackgroundColor,
                  boxShadow: [
                    BoxShadow(
                      color: Colors.black.withValues(alpha: 0.1),
                      blurRadius: 10,
                      offset: const Offset(0, -2),
                    ),
                  ],
                ),
                child: SafeArea(
                  child: Padding(
                    padding: const EdgeInsets.symmetric(
                      horizontal: 8,
                      vertical: 4,
                    ),
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                      children: [
                        IconButton(
                          icon: Icon(
                            Icons.arrow_back_ios,
                            color: canGoBack ? null : Colors.grey,
                          ),
                          onPressed: canGoBack
                              ? () => webViewController?.goBack()
                              : null,
                        ),
                        IconButton(
                          icon: Icon(
                            Icons.arrow_forward_ios,
                            color: canGoForward ? null : Colors.grey,
                          ),
                          onPressed: canGoForward
                              ? () => webViewController?.goForward()
                              : null,
                        ),
                        IconButton(
                          icon: const Icon(Icons.refresh),
                          onPressed: () => webViewController?.reload(),
                        ),
                        IconButton(
                          icon: const Icon(Icons.home),
                          onPressed: () {
                            webViewController?.loadUrl(
                              urlRequest: URLRequest(url: WebUri(url)),
                            );
                          },
                        ),
                        IconButton(
                          icon: const Icon(Icons.share),
                          onPressed: () async {
                            final currentUrl =
                                await webViewController?.getUrl();
                            if (currentUrl != null) {
                              await share_plus.Share.share(
                                currentUrl.toString(),
                              );
                            }
                          },
                        ),
                      ],
                    ),
                  ),
                ),
              ),
      ),
    );
  }

  Widget _buildOfflineWidget() {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(Icons.wifi_off, size: 80, color: Colors.grey[400]),
          const SizedBox(height: 20),
          Text(
            'No Internet Connection',
            style: TextStyle(
              fontSize: 20,
              fontWeight: FontWeight.bold,
              color: Colors.grey[600],
            ),
          ),
          const SizedBox(height: 10),
          Text(
            'Please check your connection and try again',
            style: TextStyle(fontSize: 14, color: Colors.grey[500]),
          ),
          const SizedBox(height: 30),
          ElevatedButton.icon(
            onPressed: () async {
              await _checkConnectivity();
              if (!isOffline) {
                webViewController?.reload();
              }
            },
            icon: const Icon(Icons.refresh),
            label: const Text('Retry'),
          ),
        ],
      ),
    );
  }
}
