import 'package:flutter/material.dart';

import '../../../../shared/widgets/widgets.dart';

/// User wallet screen. Add money, view balance. Aligns with POST /api/v1/users/wallet/add-money.
class UserWalletScreen extends StatelessWidget {
  const UserWalletScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return AppScaffold(
      title: 'Wallet',
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Card(
            child: Padding(
              padding: const EdgeInsets.all(24),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'Balance',
                    style: Theme.of(context).textTheme.titleSmall?.copyWith(
                          color: Theme.of(context).colorScheme.onSurfaceVariant,
                        ),
                  ),
                  const SizedBox(height: 4),
                  Text(
                    '₹ 0',
                    style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                          fontWeight: FontWeight.bold,
                        ),
                  ),
                ],
              ),
            ),
          ),
          const SizedBox(height: 24),
          Text(
            'Add money',
            style: Theme.of(context).textTheme.titleMedium,
          ),
          const SizedBox(height: 12),
          Wrap(
            spacing: 12,
            runSpacing: 12,
            children: ['100', '250', '500', '1000'].map((amount) {
              return ActionChip(
                label: Text('₹ $amount'),
                onPressed: () {
                  // TODO: POST /api/v1/users/wallet/add-money
                  ScaffoldMessenger.of(context).showSnackBar(
                    SnackBar(content: Text('Add ₹$amount — integrate payment')),
                  );
                },
              );
            }).toList(),
          ),
        ],
      ),
    );
  }
}
