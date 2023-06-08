const axios = require('axios');
const cheerio = require('cheerio');
const argparse = require('argparse');
const sleep = require('util').promisify(setTimeout);

async function crawlWeb(url, word, depth) {
  const visited = new Set();
  const queue = [{ url, level: 0 }];
  let totalCount = 0;

  while (queue.length > 0) {
    const { url, level } = queue.shift();
    if (level > depth) {
      break;
    }

    if (visited.has(url)) {
      continue;
    }

    visited.add(url);
    console.log(`Crawling: ${url}`);

    try {
      const response = await axios.get(url);
      const bodyText = response.data;

      // Count the occurrences of the word
      const wordCount = (bodyText.match(new RegExp(word, 'gi')) || []).length;
      totalCount += wordCount;
      console.log(`Occurrences of '${word}' on ${url}: ${wordCount}`);

      // Extract links from the webpage
      const $ = cheerio.load(bodyText);
      const links = $('a');
      links.each((index, element) => {
        const href = $(element).attr('href');
        if (href && href.startsWith('http')) {
          queue.push({ url: href, level: level + 1 });
        }
      });

      // Delay between requests to mimic human-like behavior
      await sleep(2000);
    } catch (error) {
      console.error(`An error occurred while accessing ${url}: ${error.message}`);
    }
  }

  console.log(`\nTotal occurrences of '${word}' across all pages: ${totalCount}`);
}

const parser = new argparse.ArgumentParser({ description: 'Web Crawler' });
parser.add_argument('url', { type: String, help: 'URL to crawl' });
parser.add_argument('word', { type: String, default: 'kayako', nargs: '?', help: 'Word to search for' });
parser.add_argument('depth', { type: Number, default: 2, nargs: '?', help: 'Scan depth level' });
const args = parser.parse_args();

crawlWeb(args.url, args.word, args.depth);
