import { dirname } from 'path';
import { fileURLToPath } from 'url';
import { FlatCompat } from '@eslint/eslintrc';
import boundariesPlugin from 'eslint-plugin-boundaries';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const compat = new FlatCompat({
  baseDirectory: __dirname,
});

// Extending Next.js core configurations
const eslintConfig = [
  ...compat.extends(
    'next/core-web-vitals', 
    'next/typescript',
    'plugin:node/recommended'
  ),
  {
    settings: {
      'boundaries/include': ['src/**/*'],
      'boundaries/elements': [
        {
          mode: 'full',
          type: 'shared',
          pattern: [
            'src/components/**/*',
            'src/data/**/*',
            'src/drizzle/**/*',
            'src/hooks/**/*',
            'src/lib/**/*',
            'src/server/**/*',
            'src/database/**/*',
          ],
        },
        {
          mode: 'full',
          type: 'feature',
          capture: ['featureName'],
          pattern: ['src/features/*/**/*'],
        },
        {
          mode: 'full',
          type: 'app',
          capture: ['_', 'fileName'],
          pattern: ['src/app/**/*'],
        },
        {
          mode: 'full',
          type: 'neverImport',
          pattern: ['src/*', 'src/tasks/**/*'],
        },
      ],
    },
    rules: {
      'boundaries/no-unknown': 'error',
      'boundaries/no-unknown-files': 'error',
      'boundaries/element-types': [
        'error',
        {
          default: 'disallow',
          rules: [
            {
              from: ['shared'],
              allow: ['shared'],
            },
            {
              from: ['feature'],
              allow: [
                'shared',
                ['feature', { featureName: '${from.featureName}' }],
              ],
            },
            {
              from: ['app', 'neverImport'],
              allow: ['shared', 'feature'],
            },
            {
              from: ['app'],
              allow: [['app', { fileName: '*.css' }]],
            },
          ],
        },
      ],
      'node/no-unsupported-features/es-syntax': ['error', { version: '20.18.3' }],
    },
    plugins: {
      boundaries: boundariesPlugin,
    },
  },
];

export default eslintConfig;
