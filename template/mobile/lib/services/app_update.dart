// app auto update popup, don't change the source code

import 'dart:io' show Platform;
import 'package:flutter/material.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter_app_version_checker/flutter_app_version_checker.dart';
import 'package:open_store/open_store.dart';

final checker = AppVersionChecker();

void checkAppUpdate(
    BuildContext context, String iosAppId, String androidAppId) async {
  checker.checkUpdate().then(
    (value) {
      if (value.canUpdate) {
        updateNow(context, iosAppId, androidAppId);
      } else {
        // ignore: avoid_print
        print('No update available');
      }
    },
  );
}

Future<void> updateNow(
  BuildContext context,
  String iosAppId,
  String androidAppId,
) async {
  if (Platform.isAndroid) {
    showDialog(
      context: context,
      builder: (context) {
        return AlertDialog(
          title: const Text('Update Available'),
          content: const Text(
              'There\'s an update available. Please update the app to continue using it.'),
          actions: <Widget>[
            TextButton(
              onPressed: () {
                OpenStore.instance.open(
                  androidAppBundleId: androidAppId,
                );
              },
              child: const Text('Update'),
            ),
            TextButton(
              onPressed: () {
                Navigator.pop(context);
              },
              child: const Text('Cancel'),
            )
          ],
        );
      },
    );
  } else if (Platform.isIOS) {
    showCupertinoDialog(
      context: context,
      builder: (context) => CupertinoAlertDialog(
        title: const Text('Update Available'),
        content: const Text(
            'There\'s an update available. Please update the app to continue using it.'),
        actions: <Widget>[
          CupertinoDialogAction(
            child: const Text('Cancel'),
            onPressed: () {
              Navigator.pop(context);
            },
          ),
          CupertinoDialogAction(
            child: const Text(
              'Update',
            ),
            onPressed: () {
              OpenStore.instance.open(
                appStoreId: iosAppId,
              );
              Navigator.pop(context);
            },
          ),
        ],
      ),
    );
  } else {}
}
