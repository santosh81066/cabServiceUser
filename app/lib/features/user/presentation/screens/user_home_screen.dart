import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

import '../../../../core/router/app_router.dart';
import '../../../../shared/widgets/widgets.dart';
import '../widgets/user_menu_tile.dart';

/// User (PAX) home screen after login. Entry point for booking and profile.
class UserHomeScreen extends StatelessWidget {
  const UserHomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return AppScaffold(
      title: 'Cab Service',
      actions: [
        IconButton(
          icon: const Icon(Icons.person_outline),
          onPressed: () => context.push(AppRoutes.userProfile),
        ),
      ],
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          UserMenuTile(
            icon: Icons.account_balance_wallet_outlined,
            title: 'Wallet',
            subtitle: 'Add money, view balance',
            onTap: () => context.push(AppRoutes.userWallet),
          ),
          const SizedBox(height: 8),
          UserMenuTile(
            icon: Icons.location_on_outlined,
            title: 'Saved places',
            subtitle: 'Home, work, favourites',
            onTap: () => context.push(AppRoutes.userSavedPlaces),
          ),
          const SizedBox(height: 8),
          UserMenuTile(
            icon: Icons.directions_car_outlined,
            title: 'Book a ride',
            subtitle: 'Single, sharing, outstation',
            onTap: () {
              // TODO: Navigate to ride booking flow
            },
          ),
        ],
      ),
    );
  }
}
