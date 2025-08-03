# client/Dockerfile

FROM node:20-alpine AS build

# Set working directory
WORKDIR /app

# Copy only necessary files for npm install first (for caching)
COPY package.json package-lock.json ./
RUN npm install

# Now copy rest of the app
COPY . .
RUN npm run build

# Final production image using NGINX
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
