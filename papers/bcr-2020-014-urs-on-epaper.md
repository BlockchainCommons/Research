# URs on E-Paper Display

## BCR-2020-014

**© 2020 Blockchain Commons**

Authors: Gorazd Kovacic, Christopher Allen<br/>
Date: October 1, 2020


## Abstract

This paper investigates running QR animations standardized in [bcr-2020-005-ur](https://github.com/BlockchainCommons/Research/blob/master/papers/bcr-2020-005-ur.md) and [bc-ur](https://github.com/BlockchainCommons/bc-ur/) on ATSAMD51J20 ([bc-lethekit](https://github.com/BlockchainCommons/bc-lethekit)) on an e-paper display [1.54inch-e-Paper-Module Rev. 2.1](https://www.waveshare.net/w/upload/e/e5/1.54inch_e-paper_V2_Datasheet.pdf) (200x200).

The results suggest we can animate 1 QR code per second or up to 2 if the QR parts are very small.
Another finding is that *UREncoder* gets very slow (4 seconds) for messages of size around 5kB and 100 byte QR parts.

## Introduction

The advantage of e-paper displays is they use very little power or no power at all when displaying a static image. This comes at a cost of a display's refresh rate capabilities.
Most e-paper displays need a couple of seconds to do a full refresh cycle and some of them are able to do a partial refresh cycle which are faster but less clean. That is you can still
see some small remnants of a previous image which is good enough for many applications, including animation of QR codes.

![img](https://i.ibb.co/g4pmJbr/epaper.jpg)

### Libraries used

* The bc-ur library has been ported to work with Arduino (bc-ur-arduino) and can be found in [bc-lethekit/deps](https://github.com/BlockchainCommons/bc-lethekit/tree/master/deps).
* The display library used in lethekit is [GxEPD2_154_D67](https://github.com/ZinggJM/GxEPD2) and suggests that the screen has a partial refresh time of 500 ms:

```bash
$ git grep partial_refresh_time
src/epd/GxEPD2_1248.cpp:  _waitWhileAnyBusy("_Update_Part", partial_refresh_time);
src/epd/GxEPD2_1248.h:    static const uint16_t partial_refresh_time = 1600; // ms, e.g. 1525001us
src/epd/GxEPD2_154.cpp:  _waitWhileBusy("_Update_Part", partial_refresh_time);
src/epd/GxEPD2_154.h:    static const uint16_t partial_refresh_time = 300; // ms, e.g. 290867us
src/epd/GxEPD2_154_D67.cpp:  _waitWhileBusy("_Update_Part", partial_refresh_time);
src/epd/GxEPD2_154_D67.h:    static const uint16_t partial_refresh_time = 500; // ms, e.g. 457282us
```

*Note:* there is also GxEPD2_154 screen which works with lethekit and has a refresh time of 300 ms. This screen is discontinued, hence no measurements were conducted with it.

## Measurements

In this section the code is introduced used to measure the rate of QR animations with different parameters.
We are conveying a message (*message_size*) split into qr parts (*CHUNK_SIZE*) by the *UR encoder*. The QR code can fully fit
onto screen (*scale* = 200) or we can make it smaller.

*Note:* scale is not a reliable parameter. Scale of 200 means display the QR code over the whole screen if possible. The actually depicted code may
be smaller.


*displayQR* is a function which generates the QR "pixels" and sends them over to the display's RAM one by one rather than as a whole. This is usually
how it's done on devices with low RAM resources.


```cpp
void ur_demo(void) {

    uint32_t dt;
    uint32_t dt0;
    const size_t CHUNK_SIZE = 100; // bytes

    dt = millis();
    auto ur = make_message_ur(5000);
    dt = millis() - dt;
    Serial.println("Make mesage: " + String(dt));

    dt = millis();
    auto encoder = UREncoder(ur, CHUNK_SIZE);
    dt = millis() - dt;
    Serial.println("UREncoder: " + String(dt));

    while (true) {

      // measure refresh rate
      dt0 = millis();

      dt = millis();
      string _part = encoder.next_part();
      dt = millis() - dt;
      Serial.println("Encoder.next_part: " + String(dt));

      const char * part_tmp = _part.c_str();
      String part_Str = part_tmp;
      part_Str.toUpperCase();

      g_display->firstPage();
      do
      {
          g_display->setPartialWindow(0, 0, 200, 200);
          g_display->fillScreen(GxEPD_WHITE);
          g_display->setTextColor(GxEPD_BLACK);

          // measure QR generation/transfer to screen RAM
          dt = millis();
          displayQR((char *)part_Str.c_str(), 200);
          // Delta time
          dt = millis() - dt;
          Serial.println("QR Code generated: " + String(dt));
      }
      while (g_display->nextPage());

      // Delta time
      dt0 = millis() - dt0;
      Serial.println("QR updated: " + String(dt0));

      char key;
      key = g_keypad.getKey();

      switch (key) {
        case NO_KEY:
            break;
        default:
            // return on any key
            g_uistate = SEEDLESS_MENU;
            return;
      }
    }
}
```



## Results

Scale: 200

Chunk size [byte] | Refresh rate [ms]| QR generation [ms]
--- | --- | ---
50 | 717 | 155
100 | 758 | 197
200 | 861 | 296

------

Scale: 100

Chunk size [byte] | Refresh rate [ms]| QR generation [ms]
--- | --- | ---
50 | 680 | 120
100 | 723 | 161
200 | 836 | 272

-----

Chunk size: 100

Msg size [byte]| make_message_ur() [ms]| UREncoder() [ms]
--- | --- | ---
100 | 1 | 0
500 | 8 | 8
1000 | 23 | 42
2000 | 72 | 278
5000 | 384 | 3869


*Note:* printing strings over serial (`Serial.println`) is negligible (<1ms) whereas `encoder.next_part()` takes 2-3ms

We can see that the difference between refresh rate and QR generation is about **560 ms** which is close (delta=60ms) to what the refresh rate
specified for this display is.

The refresh rate of QR parts is slowing down with their size. That is because the *displayQR* function has more "pixels" to generate and send to the
display controller.


## Video

[![Urs on lethekit](https://i.ibb.co/b35PPvs/epaperdisp.png)](https://lbry.tv/URs-on-LetheKit:d "URs on lethekit")

## References

* [bcr-2020-005-ur](https://github.com/BlockchainCommons/Research/blob/master/papers/bcr-2020-005-ur.md)
* [bc-lethekit](https://github.com/BlockchainCommons/bc-lethekit)
* [GxEPD2 Arduino library](https://github.com/ZinggJM/GxEPD2)
* [datasheet_1.54V2](https://www.waveshare.net/w/upload/e/e5/1.54inch_e-paper_V2_Datasheet.pdf)
