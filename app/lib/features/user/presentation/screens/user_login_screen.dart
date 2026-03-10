import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

import '../../../../core/router/app_router.dart';
import '../../../../shared/widgets/widgets.dart';

/// User (PAX) login: phone number + OTP. Aligns with backend send-otp / verify-otp or Firebase Phone Auth.
class UserLoginScreen extends StatefulWidget {
  const UserLoginScreen({super.key});

  @override
  State<UserLoginScreen> createState() => _UserLoginScreenState();
}

class _UserLoginScreenState extends State<UserLoginScreen> {
  final _formKey = GlobalKey<FormState>();
  final _phoneController = TextEditingController();
  final _otpController = TextEditingController();

  bool _otpSent = false;
  bool _loading = false;
  String _countryCode = '+91';

  @override
  void dispose() {
    _phoneController.dispose();
    _otpController.dispose();
    super.dispose();
  }

  Future<void> _sendOtp() async {
    if (!_formKey.currentState!.validate()) return;
    setState(() => _loading = true);
    // TODO: call POST /api/v1/auth/user/send-otp
    await Future.delayed(const Duration(milliseconds: 600));
    if (mounted) {
      setState(() {
        _loading = false;
        _otpSent = true;
      });
    }
  }

  Future<void> _verifyOtp() async {
    if (!_formKey.currentState!.validate()) return;
    setState(() => _loading = true);
    // TODO: call POST /api/v1/auth/user/verify-otp or firebase-login
    await Future.delayed(const Duration(milliseconds: 800));
    if (mounted) {
      setState(() => _loading = false);
      context.go(AppRoutes.userHome);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.symmetric(horizontal: 24),
          child: Form(
            key: _formKey,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                const SizedBox(height: 48),
                Text(
                  _otpSent ? 'Enter OTP' : 'Sign in',
                  style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                        fontWeight: FontWeight.bold,
                      ),
                ),
                const SizedBox(height: 8),
                Text(
                  _otpSent
                      ? 'We sent a code to $_countryCode ${_phoneController.text}'
                      : 'Enter your phone number to continue',
                  style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                        color: Theme.of(context).colorScheme.onSurfaceVariant,
                      ),
                ),
                const SizedBox(height: 32),
                if (!_otpSent) ...[
                  AppTextField(
                    controller: _phoneController,
                    label: 'Phone number',
                    hint: '9899999921',
                    keyboardType: TextInputType.phone,
                    prefix: Text(_countryCode),
                    validator: (v) {
                      if (v == null || v.length < 10) return 'Enter a valid phone number';
                      return null;
                    },
                  ),
                  const SizedBox(height: 24),
                  AppButton(
                    label: 'Send OTP',
                    onPressed: _sendOtp,
                    loading: _loading,
                  ),
                ] else ...[
                  AppTextField(
                    controller: _otpController,
                    label: 'OTP',
                    hint: '123456',
                    keyboardType: TextInputType.number,
                    maxLength: 6,
                    textInputAction: TextInputAction.done,
                    validator: (v) {
                      if (v == null || v.length != 6) return 'Enter 6-digit OTP';
                      return null;
                    },
                  ),
                  const SizedBox(height: 24),
                  AppButton(
                    label: 'Verify & continue',
                    onPressed: _verifyOtp,
                    loading: _loading,
                  ),
                  const SizedBox(height: 16),
                  TextButton(
                    onPressed: () => setState(() => _otpSent = false),
                    child: const Text('Change number'),
                  ),
                ],
              ],
            ),
          ),
        ),
      ),
    );
  }
}
