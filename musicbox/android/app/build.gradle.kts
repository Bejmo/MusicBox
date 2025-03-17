plugins {
    id("com.android.application")
    id("com.chaquo.python") version "12.0.1"
    id("kotlin-android")
    // The Flutter Gradle Plugin must be applied after the Android and Kotlin Gradle plugins.
    id("dev.flutter.flutter-gradle-plugin")
}

android {
    namespace = "com.example.musicbox"
    compileSdk = flutter.compileSdkVersion
    ndkVersion = flutter.ndkVersion

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_11
        targetCompatibility = JavaVersion.VERSION_11
    }

    kotlinOptions {
        jvmTarget = JavaVersion.VERSION_11.toString()
    }

    defaultConfig {
        applicationId = "com.example.musicbox"
        minSdk = flutter.minSdkVersion
        targetSdk = flutter.targetSdkVersion
        versionCode = flutter.versionCode
        versionName = flutter.versionName
    }

    buildTypes {
        release {
            signingConfig = signingConfigs.getByName("debug")
        }
    }
}

flutter {
    source = "../.."
}

dependencies {
    implementation("com.chaquo.python:gradle:12.0.1")
}

chaquopy {
    pythonVersion = "3.8"  // O la versión que desees usar, debe ser compatible con Chaquopy
}

python {
    buildPython("3.8")  // Especifica la versión que deseas utilizar para tu proyecto
    pip {
        install("yt-dlp")  // Para descargar vídeos desde YouTube
        install("mutagen")  // Para modificar metadatos de audio
    }
}
