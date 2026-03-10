import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

import '../../features/user/presentation/screens/user_home_screen.dart';
import '../../features/user/presentation/screens/user_login_screen.dart';
import '../../features/user/presentation/screens/user_profile_screen.dart';
import '../../features/user/presentation/screens/user_saved_places_screen.dart';
import '../../features/user/presentation/screens/user_wallet_screen.dart';

abstract class AppRoutes {
  static const String login = '/login';
  static const String userHome = '/user/home';
  static const String userProfile = '/user/profile';
  static const String userWallet = '/user/wallet';
  static const String userSavedPlaces = '/user/saved-places';
}

final class AppRouter {
  static final GoRouter router = GoRouter(
    initialLocation: AppRoutes.login,
    routes: <RouteBase>[
      GoRoute(
        path: AppRoutes.login,
        name: 'login',
        builder: (BuildContext context, GoRouterState state) =>
            const UserLoginScreen(),
      ),
      GoRoute(
        path: AppRoutes.userHome,
        name: 'userHome',
        builder: (BuildContext context, GoRouterState state) =>
            const UserHomeScreen(),
      ),
      GoRoute(
        path: AppRoutes.userProfile,
        name: 'userProfile',
        builder: (BuildContext context, GoRouterState state) =>
            const UserProfileScreen(),
      ),
      GoRoute(
        path: AppRoutes.userWallet,
        name: 'userWallet',
        builder: (BuildContext context, GoRouterState state) =>
            const UserWalletScreen(),
      ),
      GoRoute(
        path: AppRoutes.userSavedPlaces,
        name: 'userSavedPlaces',
        builder: (BuildContext context, GoRouterState state) =>
            const UserSavedPlacesScreen(),
      ),
    ],
  );
}
