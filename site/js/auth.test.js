const { TestScheduler } = require('jest');
const puppeteer = require('puppeteer');
// this provides the path of the current directory so that relative filepath handling can be done
const path = require('path');

test('test login functionality', async () =>{
    jest.setTimeout(30000);
    const browser = await puppeteer.launch({
        headless: false,
        slowMo: 50,
        args: ['--start-maximized']
    })

    const page = await browser.newPage();
    await page.setViewport({ width: 1920, height: 1080});
    await page.goto(`file:${path.join(__dirname, '../index.html')}`, {waitUntil: 'load'});

    // page.click is does not reslove, using the workaround found here https://github.com/puppeteer/puppeteer/issues/3347
    await page.$eval('a#login', elem => elem.click());
    await page.type('input#login-email', 'test@example.com');
    await page.type('input#login-password', 'test12');
    await page.$eval('button#login-button', elem => elem.click());

    await browser.close();
})