# Cab Service App (Flutter)

Flutter app for Cab Service — User (PAX), Driver (DRV), and Admin (ADM) flows. Backend: `../backend`.

## Project structure

```
lib/
├── main.dart
├── app.dart
├── core/                         # App-wide config
│   ├── constants/
│   │   └── api_constants.dart
│   ├── theme/
│   │   ├── app_theme.dart
│   │   └── app_colors.dart
│   └── router/
│       └── app_router.dart
├── shared/                       # Reusable across all features
│   └── widgets/
│       ├── app_button.dart
│       ├── app_text_field.dart
│       ├── app_scaffold.dart
│       ├── loading_overlay.dart
│       └── widgets.dart          # barrel export
└── features/
    └── user/                     # User (passenger) feature
        ├── user.dart             # barrel export
        └── presentation/
            ├── screens/
            │   ├── user_login_screen.dart
            │   ├── user_home_screen.dart
            │   ├── user_profile_screen.dart
            │   ├── user_wallet_screen.dart
            │   └── user_saved_places_screen.dart
            └── widgets/
                └── user_menu_tile.dart   # reusable within user feature
```

- **Reusable widgets**: Use `shared/widgets` (e.g. `AppButton`, `AppTextField`, `AppScaffold`) in any feature. Use `features/user/presentation/widgets` for user-specific reusable pieces (e.g. `UserMenuTile`).
- **User screens** align with backend: login (OTP/Firebase), profile (PATCH `/users/me`), wallet, saved places. Add ride booking and support screens as needed.

## Run

```bash
cd app
flutter pub get
flutter run
```

If this is a new project, run `flutter create . --project-name cab_service_app` once inside `app` to generate `android/`, `ios/`, etc.

## Environment

Set API base in `lib/core/constants/api_constants.dart` or via env (e.g. `http://localhost:8000`).
