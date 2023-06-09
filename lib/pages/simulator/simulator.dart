import 'package:device_frame/device_frame.dart';
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
    return SizedBox(
      height: MediaQuery.of(context).size.height,
      width: 375,
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
    );
  }
}

class WebView extends WidgetFactory with WebViewFactory {}
