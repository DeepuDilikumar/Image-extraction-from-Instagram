const puppeteer = require('puppeteer');
const cheerio = require('cheerio');
const axios = require('axios');
const fs = require('fs')

const insta_page = 'altrollan.app';
let imageUrls = [];


username = 'divasavum.troll';
password = 'hellothere!';

(async () => {
  const browser = await puppeteer.launch({ headless: false });
  const page = await browser.newPage();
  
  await page.goto('https://www.instagram.com/');
  await page.waitForSelector('input[name="username"]');
  await page.type('input[name="username"]', username);
  await page.type('input[name="password"]', password);
  await page.click('button[type="submit"]');
  await page.waitForNavigation();

  // Navigate to Instagram profile page
 if( await page.goto('https://www.instagram.com/'+insta_page+'/'))
 	console.log('Instagram Page Visited successfully...');

  // Log in if necessary (assuming you have credentials saved somewhere)
  // ...

  // Scroll through the page and load all the images
  let previousHeight = 0;
  
  let count = 0;
  
  while (1) {
    await page.evaluate('window.scrollTo(0, document.body.scrollHeight)');
    await page.waitForTimeout(2000); // wait for images to load
    let html = await page.content();
    let $ = cheerio.load(html);
    let urls = $('img').toArray().map(elem => $(elem).attr('src'));
    
    
    // Filter out non-image URLs
    let filteredUrls = urls.filter(url => url.startsWith('https://instagram.fccj2-1.fna.fbcdn.net'));
    
    
    console.log(filteredUrls);
	

    // Add unique URLs to imageUrls array
    filteredUrls.forEach(url => {
      if (!imageUrls.includes(url)) {
        imageUrls.push(url);
        console.log(url);
      }
    });

    // Check if reached end of profile

    const currentHeight = await page.evaluate('document.body.scrollHeight');
    if (currentHeight === previousHeight) {
      break;
    }
    previousHeight = currentHeight;
    
  }

  // Download the images
  count = 0;
  for (let i = 0; i < imageUrls.length; i++) {
    const response = await axios.get(imageUrls[i], { responseType: 'stream' });
    response.data.pipe(fs.createWriteStream(`./images/image-${i}.jpg`)); // or some other filename
    count = count + 1;
  }
  
  console.log('Total number of images: '+count.toString());

  await browser.close();
})();
