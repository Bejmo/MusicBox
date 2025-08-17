package com.musicbox

import android.Manifest
import android.content.ContentValues
import android.content.pm.PackageManager
import android.os.Build
import android.os.Bundle
import android.os.Environment
import android.provider.MediaStore
import android.util.Log
import android.widget.Button
import android.widget.EditText
import android.widget.TextView
import androidx.annotation.RequiresApi
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import kotlinx.coroutines.*
import okhttp3.*
import okhttp3.MediaType.Companion.toMediaTypeOrNull
import okio.IOException
import java.io.File

class MainActivity : AppCompatActivity() {

    private val client = OkHttpClient.Builder()
        .connectTimeout(2, java.util.concurrent.TimeUnit.MINUTES) // tiempo para conectarse al servidor
        .writeTimeout(10, java.util.concurrent.TimeUnit.MINUTES)  // tiempo para enviar la petición
        .readTimeout(10, java.util.concurrent.TimeUnit.MINUTES)   // tiempo para recibir la respuesta
        .build()
    private lateinit var editTextUrl: EditText
    private lateinit var buttonDownload: Button
    private lateinit var textViewStatus: TextView
    private val serverUrl = "http://10.0.2.2:8000"

    @RequiresApi(Build.VERSION_CODES.Q)
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        editTextUrl = findViewById(R.id.editTextPlaylistUrl)
        buttonDownload = findViewById(R.id.buttonDownload)
        textViewStatus = findViewById(R.id.textViewStatus)

        // Pedir permisos de almacenamiento
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.WRITE_EXTERNAL_STORAGE)
            != PackageManager.PERMISSION_GRANTED
        ) {
            ActivityCompat.requestPermissions(
                this,
                arrayOf(Manifest.permission.WRITE_EXTERNAL_STORAGE),
                1
            )
        }

        buttonDownload.setOnClickListener {
            val url = editTextUrl.text.toString()
            if (url.isNotEmpty()) {
                downloadPlaylist(url)
            }
        }
    }

    @RequiresApi(Build.VERSION_CODES.Q)
    private fun downloadPlaylist(playlistUrl: String) {
        CoroutineScope(Dispatchers.IO).launch {
            try {
                // 1. Obtener nombre de la playlist
                val playlistName = callGetPlaylistName(playlistUrl)
                val folder = File(getExternalFilesDir("downloads/AIMP"), playlistName)
                if (!folder.exists()) folder.mkdirs()
                if (!folder.exists()) folder.mkdirs()

                // 2. Obtener lista de canciones pendientes
                val downloadedFiles = folder.list()?.toList() ?: emptyList()
                val songs = callGetSongsPlaylist(playlistUrl, downloadedFiles)

                // 3. Descargar cada canción
                for (songUrl in songs) {
                    val fileName = downloadSong(songUrl, playlistName)
                    withContext(Dispatchers.Main) {
                        textViewStatus.text = "Descargada: $fileName"
                    }
                }

                withContext(Dispatchers.Main) {
                    textViewStatus.text = "¡Descarga completada!"
                }

            } catch (e: Exception) {
                withContext(Dispatchers.Main) {
                    textViewStatus.text = "Error: ${e.message}"
                }
            }
        }
    }

    private fun callGetPlaylistName(url: String): String {
        val requestBody = RequestBody.create(
            "application/json".toMediaTypeOrNull(),
            """{"url":"$url"}"""
        )
        val request = Request.Builder()
            .url("$serverUrl/get_playlist_name/")
            .post(requestBody)
            .build()
        client.newCall(request).execute().use { response ->
            if (!response.isSuccessful) throw IOException("Error en get_playlist_name")
            return response.body?.string()?.replace("\"", "") ?: throw IOException("Nombre inválido")
        }
    }

    private fun callGetSongsPlaylist(url: String, downloaded: List<String>): List<String> {
        val downloadedJson = downloaded.joinToString(prefix = "[\"", separator = "\",\"", postfix = "\"]")
        val requestBody = RequestBody.create(
            "application/json".toMediaTypeOrNull(),
            """{"url":"$url","downloaded_files":$downloadedJson}"""
        )
        val request = Request.Builder()
            .url("$serverUrl/get_songs_playlist/")
            .post(requestBody)
            .build()
        client.newCall(request).execute().use { response ->
            if (!response.isSuccessful) throw IOException("Error en get_songs_playlist")
            val body = response.body?.string() ?: "[]"
            return body.replace("[","").replace("]","").replace("\"","").split(",").filter { it.isNotEmpty() }
        }
    }

    @RequiresApi(Build.VERSION_CODES.Q)
    private fun downloadSong(songUrl: String, playlistName: String): String {
        val requestBody = RequestBody.create(
            "application/json".toMediaTypeOrNull(),
            """{"url":"$songUrl"}"""
        )
        val request = Request.Builder()
            .url("$serverUrl/download_video/")
            .post(requestBody)
            .build()

        client.newCall(request).execute().use { response ->
            if (!response.isSuccessful) throw IOException("Error descargando $songUrl")

            val disposition = response.header("Content-Disposition") ?: "archivo.mp3"
            val fileName = disposition.substringAfter("filename=").replace("\"", "")

            val resolver = contentResolver
            val contentValues = ContentValues().apply {
                put(MediaStore.MediaColumns.DISPLAY_NAME, fileName)
                put(MediaStore.MediaColumns.MIME_TYPE, "audio/mpeg")
                put(
                    MediaStore.MediaColumns.RELATIVE_PATH,
                    Environment.DIRECTORY_DOWNLOADS + "/AIMP/$playlistName"
                )
            }

            val uri = resolver.insert(MediaStore.Downloads.EXTERNAL_CONTENT_URI, contentValues)
                ?: throw IOException("No se pudo crear el archivo en Downloads")

            response.body?.byteStream()?.use { input ->
                resolver.openOutputStream(uri)?.use { output ->
                    input.copyTo(output)
                    output.flush()
                }
            }

            Log.d("DOWNLOAD", "Archivo guardado en: $uri")
            return fileName
        }
    }

}
