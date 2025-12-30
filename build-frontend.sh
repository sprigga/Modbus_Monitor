#!/bin/bash

# Build Vue 3 + Vite frontend for production

echo "Building Vue 3 + Vite frontend..."
cd frontend-vite
npm run build
cd ..

echo "Build complete! Output in frontend-vite/dist"
echo ""
echo "To start the development server:"
echo "  cd frontend-vite && npm run dev"
echo ""
echo "To rebuild and restart Docker:"
echo "  ./docker-compose restart frontend"
