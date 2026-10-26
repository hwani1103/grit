package com.gritpractice.grit

import android.os.Handler
import android.os.Looper
import android.util.AtomicFile
import io.flutter.embedding.android.FlutterActivity
import io.flutter.embedding.engine.FlutterEngine
import io.flutter.plugin.common.MethodChannel
import java.io.File
import java.util.concurrent.Executors

class MainActivity : FlutterActivity() {
    private val executor = Executors.newSingleThreadExecutor()
    private val main = Handler(Looper.getMainLooper())
    private fun storage() = AtomicFile(File(filesDir, "grit_records.json"))
    private fun async(result: MethodChannel.Result, action: () -> Any?) {
        executor.execute {
            try { val value = action(); main.post { result.success(value) } }
            catch (e: Exception) { main.post { result.error("STORAGE", "파일을 처리하지 못했습니다.", null) } }
        }
    }
    override fun configureFlutterEngine(flutterEngine: FlutterEngine) {
        super.configureFlutterEngine(flutterEngine)
        MethodChannel(flutterEngine.dartExecutor.binaryMessenger, "com.gritpractice.grit/storage")
            .setMethodCallHandler { call, result ->
                when (call.method) {
                    "read" -> async(result) {
                        val file = storage()
                        if (!file.baseFile.exists() && !File(file.baseFile.path + ".bak").exists()) null
                        else file.openRead().use { String(it.readBytes(), Charsets.UTF_8) }
                    }
                    "write" -> {
                        val text = call.arguments as? String
                        if (text == null) result.error("ARGUMENT", "데이터 없음", null)
                        else async(result) {
                            val file = storage()
                            val stream = file.startWrite()
                            try { stream.write(text.toByteArray(Charsets.UTF_8)); file.finishWrite(stream) }
                            catch (e: Exception) { file.failWrite(stream); throw e }
                            null
                        }
                    }
                    else -> result.notImplemented()
                }
            }
    }
}
