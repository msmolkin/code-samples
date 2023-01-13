'use strict';
 
const GfApi = require('gfapi'); // const GfApi = require('../../NewAPI/index');

const GFAPI_KEY = process.env.GFAPI_KEY; // API Key
const GFAPI_SECRET = process.env.GFAPI_SECRET; // TOTP secret
const logging = {
  logLevel: 'debug' // 'trace'/'debug'/('info'/'warn'/'error')/'fatal'
}

const fs = require('fs');

// For copying with a limited number of listings (record every listing in a file + have the file for keeping my listing count below the 200 post limit)
let fileBeginning = `'use strict';
const GFAPI_KEY = process.env.GFAPI_KEY;
const GFAPI_SECRET = process.env.GFAPI_SECRET;
const GfApi = require('gfapi'); //('../../../gfapi/index');
const exec = require('child_process').exec; //EDIT
const fs = require('fs'); // EDIT
const MAX_LISTINGS = 200 - 25; // Leave some cushion room from POSTING_LIMIT imposed by Gf //End EDIT
// Create a Rocket League listing
async function main() {
    const gfapi = new GfApi(GFAPI_KEY, {
        secret: GFAPI_SECRET,
        algorithm: "SHA1",
        digits: 6,
        period: 30
    }, {
        logLevel: 'trace'  // 'fatal', 'error', 'warn', 'info', 'debug', 'trace'
    });
    
  `
let fileMiddle = `let imgur_url = "https://i.imgur.com";
  let gameflip_url = "https://gameflip.com";
  let photo_url = // imgur_url + "/xnSjL44.jpg"; // NCVR
                  gameflip_url + "/img/items/rocket-league/key.png"; // Keys
  let photo_file = 'photo_filename.jpg'
  // Create an initial listing
  let query = `
let fileEnd = `
  // Delete oldest listing before posting newest listing, if coming close to the 200-listing limit //IMPT
  exec("[[ $(wc -l <listings_file.txt) -ge " + MAX_LISTINGS + " ]] && node ../../take_listing_off_sale.js $(head -n 1 listings_file.txt) && tail -n +2 listings_file.txt > temp_listings_file && mv temp_listings_file listings_file.txt", (err, out) => {console.log(out)}); // EDIT
  exec("wc -l <listings_file.txt", (err, len) => {
     var numListings = Number(len); // EDIT
     if (numListings > MAX_LISTINGS) // EDIT
       exec("node /home/$USER/gameflip/src/customscripts/take_listing_off_sale.js $(head -n 1 listings_file.txt) && tail -n +2 listings_file.txt > temp_listings_file && mv temp_listings_file listings_file.txt", (err, out) => {console.log(out)}); // EDIT
  }) // TODO: make platform independent (no bash, all in node)
  query.tags.push('Type: Virtual')
  let listing = await gfapi.listing_post(query);
  fs.appendFile('listings_file.txt', listing.id + '\\n', (err) => {if (err) throw err; console.log("Posting listing... recorded new listing in listings_file! And removed old listing that it replaced from listing_file, if applicable (if it went over limit).")} ); // EDIT
  // End EDIT
  
  // Upload an image to show in the listing page
  gfapi.upload_photo(listing.id, photo_url, 0).then(() => {
    // Upload another image to show in the search results
    return gfapi.upload_photo(listing.id, photo_url);
    // If you want to add a second image in the listing page then uncomment the two lines below:
    // }).then(() => {
    // return gfapi.upload_photo(listing.id, second_photo_url, 1);
  }).then(() => {
    // List the listing for sale
    return gfapi.listing_status(listing.id, GfApi.LISTING_STATUS.ONSALE);
  }).catch(err => {
    console.log(err);
  });
}
// Run main() and catch any unhandled Promise errors
main().catch(err => {
    console.log('==== ERROR', err);
});`

// For copying without checking limits (Gameflip removed the 200 post limit, IIRC) just uncomment these lines
// fileBeginning = `'use strict';
// 
// const GFAPI_KEY = process.env.GFAPI_KEY;
// const GFAPI_SECRET = process.env.GFAPI_SECRET;
// 
// const GfApi = require('gfapi'); //('../../../gfapi/index');
// 
// Create a Rocket League listing
// async function main() {
// const gfapi = new GfApi(GFAPI_KEY, {
//     secret: GFAPI_SECRET,
//     algorithm: "SHA1",
//     digits: 6,
//     period: 30
// }, {
//    logLevel: 'trace'  // 'fatal', 'error', 'warn', 'info', 'debug', 'trace'
// });
//
//                                                       `
// `
// fileEnd = `
// query.tags.push('Type: Virtual')
//  let listing = await gfapi.listing_post(query);
//  
//  // Upload an image to show in the listing page
//  gfapi.upload_photo(listing.id, photo_url, 0).then(() => {
//    // Upload another image to show in the search results
//    return gfapi.upload_photo(listing.id, photo_url);
//    // If you want to add a second image in the listing page then uncomment the two lines below:
//    // }).then(() => {
//    // return gfapi.upload_photo(listing.id, second_photo_url, 1);
//  }).then(() => {
//    // List the listing for sale
//    return gfapi.listing_status(listing.id, GfApi.LISTING_STATUS.ONSALE);
//  }).catch(err => {
//    console.log(err);
//  });
// }

// Run main() and catch any unhandled Promise errors
// main().catch(err => {
//     console.log('==== ERROR', err);
// });`

var extraneous_listing_properties = {}
extraneous_listing_properties.ingame_item = ['id', 'owner', 'digital_fee', 'photo', 'cover_photo', 'status', 'commission', 'seller_id_verified', 'seller_score', 'seller_ratings', 'created', 'updated', 'version']  // if listing is a Rocket League item
extraneous_listing_properties.gift_card = ['id', 'owner', 'accept_currency', 'digital_fee', 'photo:', 'cover_photo', 'status', 'shipping_fee', 'shipping_paid_by', 'commission', 'expiration', 'comment', 'visibility', 'seller_id_verified', 'seller_score', 'seller_ratings', 'created', 'updated', 'version'] // if listing is a gift card
var useful_listing_properties = {}
useful_listing_properties.ingame_item = ['kind', 'description', 'category', 'name', 'platform', 'price', 'accept_currency', 'upc', 'tags', 'digital', 'digital_region', 'digital_deliverable', 'shipping_predefined_package', 'shipping_fee', 'shipping_paid_by', 'shipping_within_days', 'expire_in_days', 'visibility']
useful_listing_properties.gift_card = ['kind', 'name', 'category', 'platform', 'description', 'price', 'tags', 'digital', 'digital_region', 'digital_deliverable', 'shipping_within_days', 'expire_in_days', 'accept_currency']

async function main() {
  // Authenticate
  const gfapi = new GfApi(GFAPI_KEY, {
    secret: GFAPI_SECRET,
    algorithm: "SHA1",
    digits: 6,
    period: 30
  }, logging);

  let argc = process.argv.length
  let listing_to_copy = {}
  listing_to_copy.id = argc > 2 ? process.argv[2].substr(-36) : undefined;  // in case I need to copy a specific listing

    // Your Gameflip account needs to be verified and Steam connected.
    // For an inventory of Rocket League items and photo URLs, view https://gameflip.com/api/gameitem/inventory/812872018935
    
    // TODO: Automate the following: download the image in question, then upload it to imgur, then put the resulting link here (or just download it to /photos directory). Then use this, instead of listing/old_listing_id/photo, for the new_listing/photo
	  // Choose an image for your listing, which could be a URL or file path
    // let photo_url = 'https://gameflip.com' + '/img/items/rocket-league/key.png';
    // let photo_file = 'key.png';
    // Create an initial listing

    // Search listings
    let profile = await gfapi.profile_get('me');
    let owner = profile.owner

    // due to the way the index.js implements listing_of, I can eek up to one extra listing out:
    // owner = owner + "&limit=21"

    if (owner) {
      let listings = await gfapi.listing_of(owner);

      let dir = './copied'
      if (!fs.existsSync(dir)){
        fs.mkdirSync(dir);
      }

      listings.forEach(listing => {
        let filename = `./copied/${listing.id}.js`
        let stream = fs.createWriteStream(filename)
        stream.write(fileBeginning)
        
        // Remove properties that don't get included in post
        // TODO: this should be done with a dictionary/object based on GfApi's item types, instead of having two hardcoded item types. extraneous_listing_properties["DIGITAL_INGAME"] should be one object property, extraneous_listing_properties["GIFT_CARD"] should be another, etc.
        let useless_listing_properties = listing.category == "DIGITAL_INGAME" ? extraneous_listing_properties.ingame_item : extraneous_listing_properties.gift_card;
        // Copy listing photo

        let photo_url = listing.cover_photo ? listing.photo[listing.cover_photo].view_url : Object.keys(listing.photo) ? listing.photo[Object.keys(listing.photo)[0]].view_url : 'https://i.imgur.com/bsMQWGJ.png'

        useless_listing_properties.forEach(key => delete listing[key]) // TODO should set "onsale"/"ready" status based on the current status of the copied item
        listing.expire_in_days = 1; // Make listings clear every day, instead of clogging up the onsale listings

        stream.write(fileMiddle + JSON.stringify(listing))
        stream.write(`\n\n  photo_url = "${photo_url}"`)
        stream.write(fileEnd)
        // NB: listing.photo is a useful object, as is listing.cover_photo (can download from these URLs and even just post the URLs as listing photo instead of downloading)

        //console.log(listing)
        //process.exit()
        stream.close()
      })
    }
}

// Run main() and catch any unhandle Promise errors
main().catch(err => {
    console.log('==== ERROR', err);
});
