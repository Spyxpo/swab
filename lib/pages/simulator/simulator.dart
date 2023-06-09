import 'package:device_frame/device_frame.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter_widget_from_html_core/flutter_widget_from_html_core.dart';
import 'package:fwfh_webview/fwfh_webview.dart';

class Simulator extends StatelessWidget {
  final String url;

  const Simulator({
    Key? key,
    required this.url,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Stack(
      children: [
        Column(
          children: [
            const SizedBox(height: 20),
            SizedBox(
              height: MediaQuery.of(context).size.height,
              width: 360,
              child: DeviceFrame(
                device: Devices.ios.iPhone13ProMax,
                isFrameVisible: true,
                orientation: Orientation.portrait,
                screen: Column(
                  children: [
                    Container(
                      height: 33,
                      color: Colors.transparent,
                    ),
                    Expanded(
                      child: HtmlWidget(
                        '<iframe src="$url"></iframe>',
                        factoryBuilder: () => WebView(),
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ],
        ),
        Positioned(
          right: 85,
          top: 10,
          child: Column(
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.end,
                children: [
                  const SizedBox(width: 10),
                  SizedBox(
                    width: 30,
                    height: 30,
                    child: CupertinoButton(
                      padding: const EdgeInsets.all(0),
                      onPressed: () {},
                      color: Colors.grey.withOpacity(0.3),
                      child: const Icon(
                        CupertinoIcons.globe,
                        size: 20,
                        color: Colors.grey,
                      ),
                    ),
                  ),
                  const SizedBox(width: 10),
                  SizedBox(
                    width: 30,
                    height: 30,
                    child: CupertinoButton(
                      padding: const EdgeInsets.all(0),
                      onPressed: () {},
                      color: Colors.grey.withOpacity(0.3),
                      child: const Icon(
                        CupertinoIcons.folder_circle,
                        size: 20,
                        color: Colors.grey,
                      ),
                    ),
                  ),
                  const SizedBox(width: 10),
                  SizedBox(
                    width: 30,
                    height: 30,
                    child: CupertinoButton(
                      padding: const EdgeInsets.all(0),
                      onPressed: () {},
                      color: Colors.grey.withOpacity(0.3),
                      child: const Icon(
                        CupertinoIcons.refresh_circled,
                        size: 20,
                        color: Colors.grey,
                      ),
                    ),
                  ),
                  const SizedBox(width: 10),
                  SizedBox(
                    width: 30,
                    height: 30,
                    child: CupertinoButton(
                      padding: const EdgeInsets.all(0),
                      onPressed: () {},
                      color: Colors.grey.withOpacity(0.3),
                      child: const Icon(
                        CupertinoIcons.stop_circle,
                        size: 20,
                        color: Colors.grey,
                      ),
                    ),
                  ),
                  const SizedBox(width: 10),
                  SizedBox(
                    width: 30,
                    height: 30,
                    child: CupertinoButton(
                      padding: const EdgeInsets.all(0),
                      onPressed: () {},
                      color: Colors.grey.withOpacity(0.3),
                      child: const Icon(
                        CupertinoIcons.play_circle,
                        size: 20,
                        color: Colors.grey,
                      ),
                    ),
                  ),
                ],
              ),
            ],
          ),
        ),
      ],
    );
  }
}

class WebView extends WidgetFactory with WebViewFactory {}
