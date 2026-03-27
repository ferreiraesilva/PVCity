# Project Type Detection

> Detect projects with React/Vite/Tailwind on the web and FastAPI on the backend as the default path.

## Keyword Matrix

| Keywords | Project Type | Template |
|---|---|---|
| dashboard, panel, admin, management | Admin Dashboard | `react-vite-tailwind` |
| crm, customer, sales, leads | CRM | `react-fastapi-fullstack` |
| e-commerce, product, cart, checkout, payment | E-commerce | `react-fastapi-fullstack` |
| saas, subscription, billing, workspace | SaaS | `react-fastapi-fullstack` |
| landing, marketing, promotional | Landing Page | `react-vite-static` |
| portal, web app, website, frontend, spa | Web App | `react-vite-tailwind` |
| api, backend, service, rest, webhook | API Service | `python-fastapi` |
| python, fastapi, pydantic, uvicorn | Python API | `python-fastapi` |
| docs, documentation, blog | Content Site | `react-vite-static` |
| mobile, android, ios, react native | Mobile App | `react-native-app` |
| flutter, dart | Mobile App | `flutter-app` |
| desktop, electron | Desktop App | `electron-desktop` |
| cli, command line, terminal | CLI Tool | `cli-tool` |

## Detection Rules

- For web-facing product requests, prefer React/Vite templates.
- For backend/API requests, prefer FastAPI.
- Do not route standard work away from the standardized templates.
