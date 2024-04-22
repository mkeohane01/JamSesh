# Use the official lightweight Node.js 16 image.
FROM node:20-bullseye

# Set the working directory in the container
WORKDIR /app

# Copy package.json, package-lock.json and install dependencies
COPY package*.json ./
RUN npm install

# Copy the rest of your app's source code from your host to your image filesystem.
COPY . .

# Build the Next.js app. Remember to set production environment variables here if necessary.
RUN npm run build

# Next.js collects all static files into the `.next` folder after building.
# By default Next.js starts on port 3000
EXPOSE 3000

# Run the Next.js server on container start.
CMD ["npm", "start"]
