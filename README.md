## Synopsis

At the top of the file there should be a short introduction and/ or overview that explains **what** the project is. This description should match descriptions added for package managers (Gemspec, package.json, etc.)

## Code Example

Show what the library does as concisely as possible, developers should be able to figure out **how** your project solves their problem by looking at the code example. Make sure the API you are showing off is obvious, and that your code is short and concise.

## Motivation

I made this repository to centralize my Bittrex code better and store them in a structured way. Often these are scripts made out of curiousity and experiment, some of the are useful and others are not. I want to put all of these in a package so I can use them in future projects.

## Installation

Some of these examples require [TALIB](http://ta-lib.org) which can be hard to install for your specific python version. I included a docker-compose file that builds the container and mounts the source code in case you can't get it to work locally.

## Bittrex API Reference

The Bittrex API has different versions.

[Standard API (V1.1)](https://www.bittrex.com/Home/Api)
1. Used for placing orders, viewing account information - private authenticated actions
1. Useful for collecting big market overviews
1. Market information is lagged and has overhead because of the HTTP post mechanisms

[Market API (V2)](https://bittrex.com/Api/v2.0/pub/market/GetTicks?marketName=BTC-WAVES&tickInterval=ThirtyMin)
1. Undocumented API
1. Useful for collecting specific coin data
1. Sends back OHLC+V data in intervals: OneMin, FiveMin, ThirtyMin

[WebSocket API (SignalR)](http://socket.bittrex.com/signalr)
1. Undocumented API - written in SignalR
1. Collecting delta's of the market: SubscribeToExchangeDeltas()
1. Ticker updates: SubscribeToExchangeDeltas(['BTC-ETH','BTC-ZEC'])

## Tests

lol

## Contributors

To contribute or get in touch with me or my peers contact me on [Telegram](http://t.me/cryptofud)


## License

A short snippet describing the license (MIT, Apache, etc.)

