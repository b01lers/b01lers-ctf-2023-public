FROM node:18-alpine

RUN apk add chromium

# skips puppeteer installing chrome and points to correct binary
ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true \
    PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium-browser
WORKDIR /app
COPY src/package*.json ./
RUN npm install
COPY src/ .

USER node

CMD ["npm", "start"]
