import 'package:flutter/material.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:firebase_auth/firebase_auth.dart';

import 'core/network/api_client.dart';
import 'features/auth/presentation/auth_screen.dart';
import 'features/dashboard/presentation/dashboard_wrapper.dart';

// ✅ GLOBAL THEME CONTROLLER
final ValueNotifier<ThemeMode> themeNotifier = ValueNotifier(ThemeMode.light);

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp();
  runApp(const FitBotEnterprise());
}

class FitBotEnterprise extends StatelessWidget {
  const FitBotEnterprise({super.key});

  @override
  Widget build(BuildContext context) {
    return ValueListenableBuilder<ThemeMode>(
      valueListenable: themeNotifier,
      builder: (_, ThemeMode currentMode, __) {
        return MaterialApp(
          title: 'FitBot Enterprise',
          debugShowCheckedModeBanner: false,
          
          themeMode: currentMode,
          theme: ThemeData.light().copyWith(
            primaryColor: const Color(0xFF6C63FF),
            scaffoldBackgroundColor: const Color(0xFFF4F7FF),
            appBarTheme: const AppBarTheme(
              backgroundColor: Colors.transparent,
              elevation: 0,
              iconTheme: IconThemeData(color: Colors.black),
              titleTextStyle: TextStyle(color: Colors.black, fontWeight: FontWeight.w900, fontSize: 20),
            ),
            colorScheme: ColorScheme.fromSeed(seedColor: const Color(0xFF6C63FF), brightness: Brightness.light),
          ),

          darkTheme: ThemeData.dark().copyWith(
            primaryColor: const Color(0xFF00F5D4),
            scaffoldBackgroundColor: const Color(0xFF121212),
            cardColor: const Color(0xFF1E1E1E),
            appBarTheme: const AppBarTheme(
              backgroundColor: Colors.transparent,
              elevation: 0,
              iconTheme: IconThemeData(color: Colors.white),
              titleTextStyle: TextStyle(color: Colors.white, fontWeight: FontWeight.w900, fontSize: 20),
            ),
            colorScheme: ColorScheme.fromSeed(seedColor: const Color(0xFF00F5D4), brightness: Brightness.dark),
          ),

          home: const AuthGateway(),
        );
      }
    );
  }
}

class AuthGateway extends StatefulWidget {
  const AuthGateway({super.key});
  @override
  State<AuthGateway> createState() => _AuthGatewayState();
}

class _AuthGatewayState extends State<AuthGateway> {
  @override
  void initState() {
    super.initState();
    _wakeUpServer();
  }

  Future<void> _wakeUpServer() async {
    bool isAlive = await ApiClient.checkHealth();
    debugPrint("AI Engine Status: ${isAlive ? 'ONLINE' : 'WAKING UP...'}");
  }

  @override
  Widget build(BuildContext context) {
    return StreamBuilder<User?>(
      stream: FirebaseAuth.instance.authStateChanges(),
      builder: (context, snapshot) {
        if (snapshot.connectionState == ConnectionState.waiting) {
          return const Scaffold(body: Center(child: CircularProgressIndicator(color: Color(0xFF6C63FF))));
        }
        if (snapshot.hasData) return const DashboardWrapper();
        return const AuthScreen();
      },
    );
  }
}
