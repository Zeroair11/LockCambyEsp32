#include "esp_camera.h"
#include <WiFi.h>
#include <WebServer.h>
#include <HTTPClient.h>

#include "soc/soc.h"
#include "soc/rtc_cntl_reg.h"

// ======================================================
// WIFI
// ======================================================

const char* ssid = ":v";
const char* password = "ngocancut";

// ======================================================
// WEB SERVER
// ======================================================

WebServer server(80);

// ======================================================
// CAMERA MODEL
// ======================================================

#define CAMERA_MODEL_AI_THINKER

#if defined(CAMERA_MODEL_AI_THINKER)

#define PWDN_GPIO_NUM     32
#define RESET_GPIO_NUM    -1

#define XCLK_GPIO_NUM      0

#define SIOD_GPIO_NUM     26
#define SIOC_GPIO_NUM     27

#define Y9_GPIO_NUM       35
#define Y8_GPIO_NUM       34
#define Y7_GPIO_NUM       39
#define Y6_GPIO_NUM       36
#define Y5_GPIO_NUM       21
#define Y4_GPIO_NUM       19
#define Y3_GPIO_NUM       18
#define Y2_GPIO_NUM        5

#define VSYNC_GPIO_NUM    25
#define HREF_GPIO_NUM     23
#define PCLK_GPIO_NUM     22

#endif

// ======================================================
// ROOT
// ======================================================

void handleRoot() {

  server.send(
    200,
    "text/plain",
    "ESP32 CAM READY"
  );
}

// ======================================================
// CAPTURE
// ======================================================

void handleCapture() {

  Serial.println("CAPTURE REQUEST");

  camera_fb_t *fb = esp_camera_fb_get();

  if (!fb) {

    Serial.println("CAPTURE FAIL");

    server.send(
      500,
      "text/plain",
      "CAMERA ERROR"
    );

    return;
  }

  WiFiClient client = server.client();

  client.println("HTTP/1.1 200 OK");

  client.println("Content-Type: image/jpeg");

  client.println(
    "Content-Length: " + String(fb->len)
  );

  client.println("Connection: close");

  client.println();

  client.write(fb->buf, fb->len);

  esp_camera_fb_return(fb);

  Serial.println("IMAGE SENT");
}

///////////////////////////////////////////////

void handleCaptureAndUpload() {

  Serial.println("CAPTURE + UPLOAD");

  camera_fb_t *fb = esp_camera_fb_get();

  if (!fb) {

    server.send(
      500,
      "text/plain",
      "CAPTURE FAIL"
    );

    return;
  }

  HTTPClient http;

  http.begin(
    "http://10.170.234.161:5000/upload"
  );

  http.addHeader(
    "Content-Type",
    "image/jpeg"
  );

  int httpResponseCode = http.POST(
    fb->buf,
    fb->len
  );

  Serial.print("UPLOAD CODE: ");

  Serial.println(httpResponseCode);

  http.end();

  esp_camera_fb_return(fb);

  server.send(
    200,
    "text/plain",
    "UPLOAD OK"
  );
}

// ======================================================
// START CAMERA
// ======================================================

bool startCamera() {

  camera_config_t config;

  config.ledc_channel = LEDC_CHANNEL_0;

  config.ledc_timer = LEDC_TIMER_0;

  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;

  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;

  config.pin_xclk = XCLK_GPIO_NUM;

  config.pin_pclk = PCLK_GPIO_NUM;

  config.pin_vsync = VSYNC_GPIO_NUM;

  config.pin_href = HREF_GPIO_NUM;

  config.pin_sscb_sda = SIOD_GPIO_NUM;

  config.pin_sscb_scl = SIOC_GPIO_NUM;

  config.pin_pwdn = PWDN_GPIO_NUM;

  config.pin_reset = RESET_GPIO_NUM;

  // ====================================================
  // CAMERA SETTINGS
  // ====================================================

  config.xclk_freq_hz = 20000000;

  config.pixel_format = PIXFORMAT_JPEG;

  config.frame_size = FRAMESIZE_QVGA;

  config.jpeg_quality = 12;

  config.fb_count = 1;

  esp_err_t err = esp_camera_init(&config);

  if (err != ESP_OK) {

    Serial.print("CAM INIT FAIL: ");

    Serial.println(err);

    return false;
  }

  sensor_t *s = esp_camera_sensor_get();

  s->set_vflip(s, 1);

  s->set_brightness(s, 1);

  s->set_saturation(s, 0);

  Serial.println("CAMERA OK");

  return true;
}

// ======================================================
// WIFI CONNECT
// ======================================================

bool connectWiFi() {

  WiFi.mode(WIFI_STA);

  WiFi.begin(ssid, password);

  Serial.print("CONNECT WIFI");

  int timeout = 20;

  while (
    WiFi.status() != WL_CONNECTED &&
    timeout > 0
  ) {

    delay(1000);

    Serial.print(".");

    timeout--;
  }

  if (WiFi.status() == WL_CONNECTED) {

    Serial.println();

    Serial.println("WIFI OK");

    Serial.print("IP: ");

    Serial.println(WiFi.localIP());

    return true;
  }

  Serial.println();

  Serial.println("WIFI FAIL");

  return false;
}

// ======================================================
// SETUP
// ======================================================

void setup() {

  // disable brownout reset
  WRITE_PERI_REG(
    RTC_CNTL_BROWN_OUT_REG,
    0
  );

  Serial.begin(115200);

  delay(3000);

  Serial.println();

  Serial.println("BOOT");

  // ====================================================
  // CAMERA
  // ====================================================

  if (!startCamera()) {

    Serial.println("CAMERA START FAIL");

    return;
  }

  // ====================================================
  // WIFI
  // ====================================================

  if (!connectWiFi()) {

    return;
  }

  // ====================================================
  // ROUTES
  // ====================================================

  server.on("/", handleRoot);

  server.on(
    "/capture",
    HTTP_GET,
    handleCapture
  );

  server.on(
  "/capture_and_upload",
  HTTP_GET,
  handleCaptureAndUpload
  );  

  // ====================================================
  // START SERVER
  // ====================================================

  server.begin();

  Serial.println("SERVER READY");
}

// ======================================================
// LOOP
// ======================================================

void loop() {

  server.handleClient();

  delay(1);
}