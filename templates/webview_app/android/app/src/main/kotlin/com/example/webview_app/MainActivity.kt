package com.example.webview_app

import android.content.ClipData
import android.content.ClipboardManager
import android.content.Context
import io.flutter.embedding.android.FlutterActivity
import io.flutter.embedding.engine.FlutterEngine
import io.flutter.plugin.common.MethodChannel

class MainActivity : FlutterActivity() {

    private val CHANNEL = "swab/clipboard"

    override fun configureFlutterEngine(flutterEngine: FlutterEngine) {
        super.configureFlutterEngine(flutterEngine)

        MethodChannel(
            flutterEngine.dartExecutor.binaryMessenger,
            CHANNEL
        ).setMethodCallHandler { call, result ->
            when (call.method) {
                "copyText" -> {
                    val text = call.argument<String>("text")
                    if (text != null) {
                        copyToClipboard(text)
                        result.success(null)
                    } else {
                        result.error("INVALID", "Text is null", null)
                    }
                }

                "pasteText" -> {
                    val text = getFromClipboard()
                    result.success(text)
                }

                else -> result.notImplemented()
            }
        }
    }

    private fun copyToClipboard(text: String) {
        val clipboard =
            getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager
        val clip = ClipData.newPlainText("clipboard", text)
        clipboard.setPrimaryClip(clip)
    }

    private fun getFromClipboard(): String {
        val clipboard =
            getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager

        return if (clipboard.hasPrimaryClip()
            && clipboard.primaryClip != null
            && clipboard.primaryClip!!.itemCount > 0
        ) {
            clipboard.primaryClip!!.getItemAt(0).coerceToText(this).toString()
        } else {
            ""
        }
    }
}
