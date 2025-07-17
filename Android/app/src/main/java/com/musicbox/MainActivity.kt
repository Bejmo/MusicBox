package com.musicbox

import android.os.Bundle
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.widget.Button
import android.widget.EditText
import android.widget.Toast
import androidx.appcompat.app.AlertDialog
import androidx.core.content.ContextCompat
import java.io.File
import androidx.core.app.ActivityCompat
import android.Manifest
import android.os.Environment

class MainActivity : AppCompatActivity() {
    // Path variables
    private val termuxPackage = "com.termux"
    private val scriptName = "terminal_mobile.py"
    private val scriptDir by lazy {
        File(getExternalFilesDir(Environment.DIRECTORY_MUSIC), "MusicBox").absolutePath
    }
    private val scriptPath by lazy { "$scriptDir/$scriptName" }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(R.layout.activity_main)
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main)) { v, insets ->
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom)
            insets
        }

        // Initialize permissions and copy script
        getPermissions()
        copyScript()

        // Setup UI interactions
        val button = findViewById<Button>(R.id.confirmURL)
        val inputURL = findViewById<EditText>(R.id.URLinput)
        button.setOnClickListener {
            val url = inputURL.text.toString().trim()
            executePythonScript(this, url)
        }
    }

    // Request write permissions if needed
    private fun getPermissions() {
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.WRITE_EXTERNAL_STORAGE)
            != PackageManager.PERMISSION_GRANTED
        ) {
            ActivityCompat.requestPermissions(
                this,
                arrayOf(Manifest.permission.WRITE_EXTERNAL_STORAGE),
                1
            )
        }
    }

    // Copy the Python script from assets to external storage if not already copied
    private fun copyScript() {
        val directory = File(scriptDir)
        if (!directory.exists()) {
            val created = directory.mkdirs()
            if (!created) {
                showErrorDialog("Error", "Failed to create directory: $scriptDir")
                return
            }
        }

        val destination = File(scriptPath)
        if (!destination.exists()) {
            try {
                val inputStream = assets.open(scriptName)
                destination.outputStream().use { fileOut ->
                    inputStream.copyTo(fileOut)
                }
                Toast.makeText(this, "Script copied to $scriptDir", Toast.LENGTH_SHORT).show()
            } catch (e: Exception) {
                e.printStackTrace()
                showErrorDialog("Error copying script", e.message ?: "Unknown error")
            }
        } else {
            Toast.makeText(this, "Script already exists in $scriptDir", Toast.LENGTH_SHORT).show()
        }
    }

    // Execute the python script through Termux passing input string via echo
    private fun executePythonScript(context: Context, url: String) {
        // Check if Termux is installed
        val termuxInstalled = try {
            context.packageManager.getPackageInfo(termuxPackage, 0)
            true
        } catch (e: PackageManager.NameNotFoundException) {
            false
        }

        if (!termuxInstalled) {
            showErrorDialog("Error", "Termux is not installed")
            return
        }

        val escapedInput = url.replace("\"", "\\\"")
        val command = "echo \"$escapedInput\" | \\$(which python) $scriptPath"

        val intent = Intent("com.termux.RUN_COMMAND").apply {
            setClassName(termuxPackage, "com.termux.app.RunCommandService")
            putExtra("com.termux.RUN_COMMAND_PATH", "/data/data/com.termux/files/usr/bin/sh")
            putExtra("com.termux.RUN_COMMAND_ARGUMENTS", arrayOf("-c", command))
            putExtra("com.termux.RUN_COMMAND_BACKGROUND", true)
        }

        try {
            context.startService(intent)
            Toast.makeText(context, "Executing script on Termux...", Toast.LENGTH_SHORT).show()
        } catch (e: Exception) {
            e.printStackTrace()
            showErrorDialog("Failed to start Termux service", e.message ?: "Unknown error")
        }
    }

    // Show a dialog with error message
    private fun showErrorDialog(title: String, message: String) {
        AlertDialog.Builder(this)
            .setTitle(title)
            .setMessage(message)
            .setPositiveButton("OK", null)
            .show()
    }
}
