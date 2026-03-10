import 'package:flutter/material.dart';

import '../../../../shared/widgets/widgets.dart';

/// User saved places (Home, Work, etc.). Aligns with POST /api/v1/users/saved-places.
class UserSavedPlacesScreen extends StatelessWidget {
  const UserSavedPlacesScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return AppScaffold(
      title: 'Saved places',
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Card(
            child: ListTile(
              leading: const Icon(Icons.home_outlined),
              title: const Text('Home'),
              subtitle: const Text('Add address'),
              trailing: const Icon(Icons.chevron_right),
              onTap: () => _showAddPlaceSheet(context, 'Home'),
            ),
          ),
          const SizedBox(height: 8),
          Card(
            child: ListTile(
              leading: const Icon(Icons.work_outline),
              title: const Text('Work'),
              subtitle: const Text('Add address'),
              trailing: const Icon(Icons.chevron_right),
              onTap: () => _showAddPlaceSheet(context, 'Work'),
            ),
          ),
        ],
      ),
    );
  }

  void _showAddPlaceSheet(BuildContext context, String label) {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      builder: (context) => Padding(
        padding: EdgeInsets.only(
          bottom: MediaQuery.of(context).viewInsets.bottom,
        ),
        child: Padding(
          padding: const EdgeInsets.all(24),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Text('Add $label', style: Theme.of(context).textTheme.titleLarge),
              const SizedBox(height: 16),
              AppTextField(
                label: 'Address',
                hint: 'e.g. HSR Layout, Bengaluru',
              ),
              const SizedBox(height: 16),
              AppButton(
                label: 'Save',
                onPressed: () {
                  Navigator.pop(context);
                  ScaffoldMessenger.of(context).showSnackBar(
                    SnackBar(content: Text('$label saved — wire to API')),
                  );
                },
              ),
            ],
          ),
        ),
      ),
    );
  }
}
