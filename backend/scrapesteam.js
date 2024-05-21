const puppeteer = require('puppeteer');

async function scrapeGameDetails(appid) {
    const url = `https://store.steampowered.com/app/${appid}`;
    const browser = await puppeteer.launch({ headless: true });
    const page = await browser.newPage();
    
    // 쿠키 설정을 통해 연령 확인 우회
    await page.setCookie({
        name: 'birthtime',
        value: '28801',
        domain: '.steampowered.com',
        path: '/',
    }, {
        name: 'lastagecheckage',
        value: '1-January-1970',
        domain: '.steampowered.com',
        path: '/',
    });

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
    const browser = await puppeteer.launch({ headless: true });
    const page = await browser.newPage();
    
    // 쿠키 설정을 통해 연령 확인 우회
    await page.setCookie({
        name: 'birthtime',
        value: '28801',
        domain: '.steampowered.com',
        path: '/',
    }, {
        name: 'lastagecheckage',
        value: '1-January-1970',
        domain: '.steampowered.com',
        path: '/',
    });

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

    for (let game of similarGames) {
        try {
            const gamePageUrl = `https://store.steampowered.com/app/${game.appid}`;
            await page.goto(gamePageUrl);

            const reviewSummary = await page.evaluate(() => {
                let reviewSummaryElement = document.querySelector('.game_review_summary');
                return reviewSummaryElement ? reviewSummaryElement.innerText : 'No reviews';
            });

            game.review_summary = reviewSummary;
        } catch (e) {
            console.log(`Error scraping review summary for appid ${game.appid}: ${e}`);
            game.review_summary = 'No reviews';
        }
    }

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
