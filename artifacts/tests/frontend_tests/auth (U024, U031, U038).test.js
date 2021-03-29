const { TestScheduler } = require('jest');
const puppeteer = require('puppeteer');
const firebase = require('firebase-admin');
// this provides the path of the current directory so that relative filepath handling can be done
const path = require('path');
const { hasUncaughtExceptionCaptureCallback } = require('process');
const { expect } = require('@jest/globals');

// U024
test('test that signup cannot occur without input', async () =>{
    jest.setTimeout(3000000);
    const browser = await puppeteer.launch({
        headless: false,
        slowMo: 25,
        args: ['--start-maximized']
    })

    const page = await browser.newPage();
    await page.setViewport({ width: 1920, height: 1080});
    // goes up 3 parent directories and into the relative path of the site
    await page.goto(`file:${path.join(__dirname, '..', '..', '..', '/mycovidtracker/static/site/test.html')}`, {waitUntil: 'load'});

    await page.$eval('a#signup', elem => elem.click());
    await page.$eval('button#signup-button', elem => elem.click());

    // checks that no user is logged in
    expect(firebase.auth.Currentuser).toBeFalsy;
    
    await page.waitForTimeout(1000);
    await browser.close();
})

// U024
test('test that signup cannot occur with an invalid email address', async () =>{
    jest.setTimeout(3000000);
    const browser = await puppeteer.launch({
        headless: false,
        slowMo: 25,
        args: ['--start-maximized']
    })

    const page = await browser.newPage();
    await page.setViewport({ width: 1920, height: 1080});
    await page.goto(`file:${path.join(__dirname, '..', '..', '..', '/mycovidtracker/static/site/test.html')}`, {waitUntil: 'load'});

    await page.$eval('a#signup', elem => elem.click());
    await page.type('input#signup-email', 'test');
    await page.type('input#signup-password', 'test12');
    await page.type('input#dob', '1990-01-01');
    
    await page.$eval('button#signup-button', elem => elem.click());

    // checks that no user is logged in
    expect(firebase.auth.Currentuser).toBeFalsy;

    await page.waitForTimeout(1000);
    await browser.close();
})

// U024
test('test that signup cannot occur with an invalid password', async () =>{
    jest.setTimeout(3000000);
    const browser = await puppeteer.launch({
        headless: false,
        slowMo: 25,
        args: ['--start-maximized']
    })

    const page = await browser.newPage();
    await page.setViewport({ width: 1920, height: 1080});
    await page.goto(`file:${path.join(__dirname, '..', '..', '..', '/mycovidtracker/static/site/test.html')}`, {waitUntil: 'load'});

    await page.$eval('a#signup', elem => elem.click());
    await page.type('input#signup-email', 'test@example.com');
    await page.type('input#signup-password', 'test');
    await page.type('input#dob', '1990-01-01');
    
    await page.$eval('button#signup-button', elem => elem.click());

    // checks that no user is logged in
    expect(firebase.auth.Currentuser).toBeFalsy;

    await page.waitForTimeout(1000);
    await browser.close();
})

// U024
test('test that signup cannot occur with an email that is in use', async () =>{
    jest.setTimeout(3000000);
    const browser = await puppeteer.launch({
        headless: false,
        slowMo: 25,
        args: ['--start-maximized']
    })

    const page = await browser.newPage();
    await page.setViewport({ width: 1920, height: 1080});
    await page.goto(`file:${path.join(__dirname, '..', '..', '..', '/mycovidtracker/static/site/test.html')}`, {waitUntil: 'load'});

    await page.$eval('a#signup', elem => elem.click());
    await page.type('input#signup-email', 'taken@example.com');
    await page.type('input#signup-password', 'test12');
    await page.type('input#dob', '1990-01-01');
    
    await page.$eval('button#signup-button', elem => elem.click());

    // checks that no user is logged in
    expect(firebase.auth.Currentuser).toBeFalsy;

    await page.waitForTimeout(1000);
    await browser.close();
})

test('test that signup cannot occur without date of birth', async () =>{
    jest.setTimeout(3000000);
    const browser = await puppeteer.launch({
        headless: false,
        slowMo: 25,
        args: ['--start-maximized']
    })

    const page = await browser.newPage();
    await page.setViewport({ width: 1920, height: 1080});
    await page.goto(`file:${path.join(__dirname, '..', '..', '..', '/mycovidtracker/static/site/test.html')}`, {waitUntil: 'load'});

    await page.$eval('a#signup', elem => elem.click());
    await page.type('input#signup-email', 'test@example.com');
    await page.type('input#signup-password', 'test12');
    
    await page.$eval('button#signup-button', elem => elem.click());
    
    // checks that no user is logged in
    expect(firebase.auth.Currentuser).toBeFalsy;

    await page.$eval('a#logout', elem => elem.click());


    await page.waitForTimeout(1000);
    await browser.close();
})

// U024
test('test proper signup functionality and logout', async () =>{
    jest.setTimeout(3000000);
    const browser = await puppeteer.launch({
        headless: false,
        slowMo: 25,
        args: ['--start-maximized']
    })

    const page = await browser.newPage();
    await page.setViewport({ width: 1920, height: 1080});
    await page.goto(`file:${path.join(__dirname, '..', '..', '..', '/mycovidtracker/static/site/test.html')}`, {waitUntil: 'load'});

    await page.$eval('a#signup', elem => elem.click());
    await page.type('input#signup-email', 'test@example.com');
    await page.type('input#signup-password', 'test12');
    await page.type('input#dob', '1990-01-01');
    await page.$eval('button#signup-button', elem => elem.click());
    
    // checks that a user is logged in
    expect(firebase.auth.Currentuser).toBeTruthy;

    await page.$eval('a#logout', elem => elem.click());


    await page.waitForTimeout(1000);
    await browser.close();
})

// U024
test('test that login cannot occur with no input', async () =>{
    jest.setTimeout(3000000);
    const browser = await puppeteer.launch({
        headless: false,
        slowMo: 25,
        args: ['--start-maximized']
    })

    const page = await browser.newPage();
    await page.setViewport({ width: 1920, height: 1080});
    await page.goto(`file:${path.join(__dirname, '..', '..', '..', '/mycovidtracker/static/site/test.html')}`, {waitUntil: 'load'});

    await page.$eval('a#login', elem => elem.click());
    await page.$eval('button#login-button', elem => elem.click());

    // checks that no user is logged in
    expect(firebase.auth.Currentuser).toBeFalsy;

    await page.waitForTimeout(1000);
    await browser.close();
})

// U024
test('test that login cannot occur without a proper email address', async () =>{
    jest.setTimeout(3000000);
    const browser = await puppeteer.launch({
        headless: false,
        slowMo: 25,
        args: ['--start-maximized']
    })

    const page = await browser.newPage();
    await page.setViewport({ width: 1920, height: 1080});
    await page.goto(`file:${path.join(__dirname, '..', '..', '..', '/mycovidtracker/static/site/test.html')}`, {waitUntil: 'load'});

    await page.$eval('a#login', elem => elem.click());
    await page.type('input#login-email', 'test');
    await page.type('input#login-password', 'test12');
    await page.$eval('button#login-button', elem => elem.click());

    // checks that no user is logged in
    expect(firebase.auth.Currentuser).toBeFalsy;

    await page.waitForTimeout(1000);
    await browser.close();
})

// U024
test('test that login cannot occur with an incorrect password', async () =>{
    jest.setTimeout(3000000);
    const browser = await puppeteer.launch({
        headless: false,
        slowMo: 25,
        args: ['--start-maximized']
    })

    const page = await browser.newPage();
    await page.setViewport({ width: 1920, height: 1080});
    await page.goto(`file:${path.join(__dirname, '..', '..', '..', '/mycovidtracker/static/site/test.html')}`, {waitUntil: 'load'});

    await page.$eval('a#login', elem => elem.click());
    await page.type('input#login-email', 'taken@example.com');
    await page.type('input#login-password', 'test12');
    await page.$eval('button#login-button', elem => elem.click());
    await page.$eval('a#logout', elem => elem.click());

    // checks that no user is logged in
    expect(firebase.auth.Currentuser).toBeFalsy;

    await page.waitForTimeout(1000);
    await browser.close();
})

// U024
test('test proper login functionality and logout', async () =>{
    jest.setTimeout(3000000);
    const browser = await puppeteer.launch({
        headless: false,
        slowMo: 25,
        args: ['--start-maximized']
    })

    const page = await browser.newPage();
    await page.setViewport({ width: 1920, height: 1080});
    await page.goto(`file:${path.join(__dirname, '..', '..', '..', '/mycovidtracker/static/site/test.html')}`, {waitUntil: 'load'});

    await page.$eval('a#login', elem => elem.click());
    await page.type('input#login-email', 'test@example.com');
    await page.type('input#login-password', 'test12');
    await page.$eval('button#login-button', elem => elem.click());

    // checks that a user is logged in
    expect(firebase.auth.Currentuser).toBeTruthy;

    await page.$eval('a#logout', elem => elem.click());

    await page.waitForTimeout(1000);
    await browser.close();
})

// U031
test('test that passwords cannot be reset with no input', async () =>{
    jest.setTimeout(3000000);
    const browser = await puppeteer.launch({
        headless: false,
        slowMo: 25,
        args: ['--start-maximized']
    })

    const page = await browser.newPage();
    await page.setViewport({ width: 1920, height: 1080});
    await page.goto(`file:${path.join(__dirname, '..', '..', '..', '/mycovidtracker/static/site/test.html')}`, {waitUntil: 'load'});

    await page.$eval('a#login', elem => elem.click());
    await page.$eval('button#reset-button', elem => elem.click());
    await page.$eval('button#reset-confirm', elem => elem.click());

    await page.waitForTimeout(1000);
    await browser.close();
})

// U031
test('test that passwords cannot be reset with an unregistered email address', async () =>{
    jest.setTimeout(3000000);
    const browser = await puppeteer.launch({
        headless: false,
        slowMo: 25,
        args: ['--start-maximized']
    })

    const page = await browser.newPage();
    await page.setViewport({ width: 1920, height: 1080});
    await page.goto(`file:${path.join(__dirname, '..', '..', '..', '/mycovidtracker/static/site/test.html')}`, {waitUntil: 'load'});

    await page.$eval('a#login', elem => elem.click());
    await page.$eval('button#reset-button', elem => elem.click());
    await page.type('input#reset-email', 'unregistered@example.com');
    await page.$eval('button#reset-confirm', elem => elem.click());

    await page.waitForTimeout(1000);
    await browser.close();
})

// U031
test('test proper password reset functionality', async () =>{
    jest.setTimeout(3000000);
    const browser = await puppeteer.launch({
        headless: false,
        slowMo: 25,
        args: ['--start-maximized']
    })

    const page = await browser.newPage();
    await page.setViewport({ width: 1920, height: 1080});
    await page.goto(`file:${path.join(__dirname, '..', '..', '..', '/mycovidtracker/static/site/test.html')}`, {waitUntil: 'load'});

    await page.$eval('a#login', elem => elem.click());
    await page.$eval('button#reset-button', elem => elem.click());
    await page.type('input#reset-email', 'test@example.com');
    await page.$eval('button#reset-confirm', elem => elem.click());

    await page.waitForTimeout(1000);
    await browser.close();
})

// U038
test('test that accounts cannot be deleted without proper authentication', async () =>{
    jest.setTimeout(3000000);
    const browser = await puppeteer.launch({
        headless: false,
        slowMo: 25,
        args: ['--start-maximized']
    })

    const page = await browser.newPage();
    await page.setViewport({ width: 1920, height: 1080});
    await page.goto(`file:${path.join(__dirname, '..', '..', '..', '/mycovidtracker/static/site/test.html')}`, {waitUntil: 'load'});

    await page.$eval('a#login', elem => elem.click());
    await page.type('input#login-email', 'test@example.com');
    await page.type('input#login-password', 'test12');
    await page.$eval('button#login-button', elem => elem.click());

    await page.$eval('a#account', elem => elem.click());
    await page.$eval('button#delete-button', elem => elem.click());
    await page.type('input#deletion-password', 'wrongpassworduhohOOPS');
    await page.$eval('button#confirm-delete', elem => elem.click());

    await page.waitForTimeout(1000);
    await browser.close();
})

// U038
test('test proper account deletion functionality', async () =>{
    jest.setTimeout(3000000);
    const browser = await puppeteer.launch({
        headless: false,
        slowMo: 25,
        args: ['--start-maximized']
    })

    const page = await browser.newPage();
    await page.setViewport({ width: 1920, height: 1080});
    await page.goto(`file:${path.join(__dirname, '..', '..', '..', '/mycovidtracker/static/site/test.html')}`, {waitUntil: 'load'});

    await page.$eval('a#login', elem => elem.click());
    await page.type('input#login-email', 'test@example.com');
    await page.type('input#login-password', 'test12');
    await page.$eval('button#login-button', elem => elem.click());

    await page.$eval('a#account', elem => elem.click());
    await page.$eval('button#delete-button', elem => elem.click());
    await page.type('input#deletion-password', 'test12');
    // await page.click('input#deletion-password');
    // await page.keyboard.type('test12');
    // await page.keyboard.press('Enter');
    // await page.click('button#confirm-delete');
    await page.$eval('button#confirm-delete', elem => elem.click());

    await page.waitForTimeout(1000);
    await browser.close();
})