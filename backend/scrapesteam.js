const puppeteer = require('puppeteer');

async function scrapeGameDetails(appid) {
    const url = `https://store.steampowered.com/app/${appid}`;
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    await page.goto(url);

    const data = await page.evaluate(() => {
        let gameDetails = {};

        let nameElement = document.querySelector('.apphub_AppName');
        gameDetails.name = nameElement ? nameElement.innerText : 'No name';

        let reviewSummaryElement = document.querySelector('.game_review_summary');
        gameDetails.review_summary = reviewSummaryElement ? reviewSummaryElement.innerText : 'No reviews';

        let imageUrlElement = document.querySelector('.game_header_image_full');
        gameDetails.image_url = imageUrlElement ? imageUrlElement.src : '';

        return gameDetails;
    });

    await browser.close();
    return data;
}

async function scrapeSimilarGames(appid) {
    const url = `https://store.steampowered.com/app/${appid}`;
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    await page.goto(url);

    const similarGames = await page.evaluate(() => {
        let games = [];
        let gameElements = document.querySelectorAll('#recommended_block_content a.small_cap');

        gameElements.forEach((gameElement) => {
            let appid = gameElement.getAttribute('data-ds-appid');
            let nameElement = gameElement.querySelector('h4');
            let priceElement = gameElement.querySelector('.discount_final_price');
            let imageElement = gameElement.querySelector('.small_cap_img');

            games.push({
                appid: appid,
                name: nameElement ? nameElement.innerText : 'No name',
                price: priceElement ? priceElement.innerText : 'No price info',
                image_url: imageElement ? imageElement.src : ''
            });
        });

        return games;
    });

    await browser.close();
    return similarGames;
}

const [,, type, appid] = process.argv;

(async () => {
    let result;
    if (type === 'details') {
        result = await scrapeGameDetails(appid);
    } else if (type === 'similar') {
        result = await scrapeSimilarGames(appid);
    }

    console.log(JSON.stringify(result));
})();
