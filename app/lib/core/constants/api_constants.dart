/// API base URL. Use env or build config in production.
const String apiBaseUrl = String.fromEnvironment(
  'API_BASE_URL',
  defaultValue: 'http://localhost:8000',
);

const String apiPrefix = '/api/v1';

String get authBase => '$apiBaseUrl$apiPrefix/auth';
String get usersBase => '$apiBaseUrl$apiPrefix/users';
