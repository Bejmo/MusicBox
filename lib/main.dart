import 'dart:io';
import 'package:flutter/material.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      home: DownloadScreen(),
    );
  }
}

class DownloadScreen extends StatefulWidget {
  @override
  _DownloadScreenState createState() => _DownloadScreenState();
}

class _DownloadScreenState extends State<DownloadScreen> {
  TextEditingController urlController = TextEditingController();
  String output = "";

  void descargarVideo() async {
    String url = urlController.text.trim();
    if (url.isEmpty) return;

    setState(() {
      output = "Descargando...";
    });

    ProcessResult result = await Process.run('python', ['python/download_music.py', url]);

    setState(() {
      output = result.stdout.isNotEmpty ? result.stdout : "Error: ${result.stderr}";
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("Descargar Música")),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            TextField(
              controller: urlController,
              decoration: InputDecoration(
                labelText: "Ingrese la URL",
                border: OutlineInputBorder(),
              ),
            ),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: descargarVideo,
              child: Text("Descargar"),
            ),
            SizedBox(height: 20),
            Text(output, textAlign: TextAlign.center),
          ],
        ),
      ),
    );
  }
}
