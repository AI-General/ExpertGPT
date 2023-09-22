# Step 1: Build a React Application
# From what image we're building
FROM node:18-alpine

WORKDIR /app

# Copy the rest of the code 
# COPY package.json ./

COPY . ./
RUN yarn install

# Build the App
# RUN  yarn build

# # Step 2: Serve app with nginx server
# FROM nginx:1.19.3-alpine
# COPY --from=build /app/build /usr/share/nginx/html

# Use non-root 
# RUN chown -R nginx /usr/share/nginx/html
# USER nginx

EXPOSE 8080
CMD ["yarn", "start"]
