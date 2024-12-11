# Stage 1: Build the React app
FROM node:16 AS build
WORKDIR /app
COPY royaldegen/package*.json ./
RUN npm install
COPY royaldegen/ .
RUN npm run build

# Stage 2: Serve with Nginx
FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
