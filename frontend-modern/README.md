# Modern Frontend for MarketData API

This is a modern, TypeScript-based frontend for the MarketData API built with Vite and Tailwind CSS.

## 🚀 Features

- **Modern Tech Stack**: Vite + TypeScript + Tailwind CSS
- **Responsive Design**: Mobile-first approach with Tailwind
- **Type Safety**: Full TypeScript coverage for API calls
- **Fast Development**: Hot reload and instant feedback
- **Component Architecture**: Reusable Web Components
- **API Integration**: Type-safe API calls to backend

## 📦 Prerequisites

Before running this frontend, you need:

1. **Node.js** (version 18 or higher)
2. **npm** or **yarn** package manager
3. **MarketData API backend** running on `http://localhost:5000`

## 🛠️ Installation

1. **Install Node.js** (if not already installed):
   - Download from [nodejs.org](https://nodejs.org/)
   - Or use a package manager like `winget install OpenJS.NodeJS`

2. **Install dependencies**:
   ```bash
   cd frontend-modern
   npm install
   ```

## 🏃‍♂️ Running the Application

1. **Start the development server**:
   ```bash
   npm run dev
   ```

2. **Open in browser**:
   - Main interface: `http://localhost:3000`
   - Admin interface: `http://localhost:3000/admin.html`

3. **Make sure your backend is running** on `http://localhost:5000`

## 🔧 Build for Production

1. **Build the application**:
   ```bash
   npm run build
   ```

2. **Preview the build**:
   ```bash
   npm run preview
   ```

3. **Deploy the `dist/` folder** to your web server

## 📁 Project Structure

```
frontend-modern/
├── public/                 # Static assets
│   └── favicon.svg
├── src/
│   ├── components/         # Component architecture
│   │   ├── base/          # Base component classes
│   │   │   └── BaseSearchComponent.ts
│   │   ├── tabs/          # Tab renderer system
│   │   │   ├── BaseTabRenderer.ts
│   │   │   ├── OverviewTabRenderer.ts
│   │   │   ├── LeiTabRenderer.ts
│   │   │   ├── TransparencyTabRenderer.ts
│   │   │   ├── CfiTabRenderer.ts
│   │   │   ├── VenuesTabRenderer.ts
│   │   │   ├── TabManager.ts
│   │   │   └── index.ts
│   │   ├── ComprehensiveSearchComponent.ts
│   │   ├── SearchComponent.ts
│   │   └── index.ts
│   ├── services/          # Business logic services
│   │   ├── InstrumentDataService.ts
│   │   └── index.ts
│   ├── utils/             # Utility functions
│   │   ├── formatters/    # Data formatting utilities
│   │   │   ├── dataFormatters.ts
│   │   │   └── index.ts
│   │   ├── api.ts         # API integration
│   │   └── helpers.ts     # Helper functions
│   ├── styles/            # CSS styles
│   │   └── main.css
│   ├── types/             # TypeScript type definitions
│   │   └── api.ts
│   ├── admin.ts           # Admin interface entry
│   └── main.ts            # Main interface entry
├── index.html             # Main interface
├── admin.html             # Admin interface
├── package.json
├── tsconfig.json          # TypeScript configuration
├── tailwind.config.js     # Tailwind CSS configuration
├── postcss.config.js      # PostCSS configuration
└── vite.config.ts         # Vite configuration
```

## 🎨 Styling

The frontend uses **Tailwind CSS** for styling with custom component classes:

- `.btn` - Button styles (primary, secondary, danger)
- `.input-field` - Form input styles
- `.card` - Card container styles
- `.alert` - Alert/notification styles
- `.tab-button` - Tab navigation styles

## 🔗 API Integration

The frontend communicates with the backend API using typed functions:

- `instrumentApi.search()` - Search instruments
- `instrumentApi.create()` - Create new instruments
- `transparencyApi.getByIsin()` - Get transparency data
- `fileApi.upload()` - Upload files

## 🧪 Development

### Architecture Overview

The frontend uses a modular architecture with clear separation of concerns:

- **Base Components**: Reusable abstract classes providing common functionality
- **Tab Renderers**: Specialized components for rendering different data views
- **Services**: Business logic and API communication layer
- **Formatters**: Utility functions for data presentation

### Adding New Components

1. **For new search components**: Extend `BaseSearchComponent` in `src/components/base/`
2. **For new tab renderers**: Extend `BaseTabRenderer` in `src/components/tabs/`
3. **For reusable UI**: Create new components in `src/components/`

### Adding New Tab Types

1. Create a new renderer extending `BaseTabRenderer`
2. Implement required methods: `render()`, `getTabId()`, `getTabLabel()`
3. Add optional methods: `getBadgeCount()`, `isEnabled()`
4. Register with `TabManager` in the constructor

### Adding New API Endpoints

1. Add types to `src/types/api.ts`
2. Add service methods to appropriate service class or create new service
3. Use services in components with full type safety

### Adding Data Formatters

1. Add formatting functions to `src/utils/formatters/dataFormatters.ts`
2. Export from `src/utils/formatters/index.ts`
3. Import and use in tab renderers or components

### Customizing Styles

1. Modify `tailwind.config.js` for theme customization
2. Add custom CSS in `src/styles/main.css`
3. Use Tailwind's `@apply` directive for component styles

## 🔒 Production Considerations

1. **Environment Variables**: Configure API endpoints for production
2. **HTTPS**: Ensure secure connections in production
3. **CSP**: Implement Content Security Policy headers
4. **Caching**: Configure appropriate cache headers
5. **Compression**: Enable gzip/brotli compression

## 🤝 Integration with Flask Backend

The frontend is designed to work alongside your existing Flask backend:

1. **Keep Flask backend** for API endpoints
2. **Serve static files** from Flask or separate web server
3. **Proxy API calls** through Vite during development
4. **CORS configuration** may be needed for cross-origin requests

## 📊 Monitoring

For production monitoring, consider adding:

- Error tracking (e.g., Sentry)
- Performance monitoring
- User analytics
- API response time tracking

---

**Happy coding! 🚀**
