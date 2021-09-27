<h1 align="center">treeHouse</h1>

Live website :arrow_down:<br>
<a href="https://treehouse-shop.herokuapp.com/">View live project here.</a>

## About

This is an e-commerce website for a fictional eco-homeware business. The goal of the website is to allow customers to browse products, create an account, purchase products and store information about themselves, their purchase history and items they want to add to a wishlist. Also the site administrator can exercise CRUD functionality on products, and blogs for customers to read and comment on. It features STRIPE's payments processer and will allow a user to make a purchase using the following card details; card num: 4242 4242 4242 4242, any date and any cvv. Submition of those details will complete the order, please don't use your own card details.

## Screenshots


## User Experience

### User Stories

- Customers
  - Website experience
    - As a customer, I would like to see what the website is selling.
    - I would like to be able to navigate the website easily.
    - I would like to see some information about the company.
    - As a customer, I would like to be able to contact the company.
  
  - Product.
    - As a customer, I would like to see all the products the company sells.
    - I would like to be able to search by category.
    - I would like to be able to search through the products.
    - I would like to sort the items by price.

  - Shopping.
    - As a customer, I would like to see the product price and description.
    - I would like to be able to add products to my shopping cart.
    - I would like to be notified when I complete interactions with the site.
    - I would like to be able to edit my shopping cart.
    - I would like to be able to checkout easily.
    - I would like to receive confirmation of my order.

  - Account.
    - As a customer, I would like to save my details to an account.
    - I would like to see my previous order details.
    - I would like to leave a review of the company.

- Website administrator.
  - As a site administrator, I would like to be able to edit and add products easily.
  - I would like to be able to delete products.
  - I would like to have access to an admin section. 
  - I would like my customers to be able to shop on the site easily.

## Mockups

### Mobile

### Tablet

### Desktop

## Database Models

- #### Models
- Profiles
  - User
    - From Django Allauth; contains their username, email, and password.
  - Userprofile
    - Model containing the user's address, phone number and username.
 
- Favourites
  - Users' Favourites
    - Contains products that the user has added to their favourites list.

- Products 
  - Products
    - Contains all the information for each product.
  - Categories
    - The categories all the products fall in to.

- Checkout
  - Order
    - Contains the details of orders a customer has made and the products they've purchased.
  - Orderline item
    - Products of the customer order, quantities and the total price.

- Blog
  - Post
    - Contains blog posts, their title and author.
  - Comments
    - Contains the comments entered under each post.

- Database Diagram

  - This databse diagram shows each object, its keys and relationships between them.

## Design

- The design of the website was inspired by a treehouse with a colour scheme dominated by greens, browns and beige. This lends itself to an eco aesthetic which matches the theme of the website, sustainable homeware.

- All the different shades of green and the gradient of the beige background with spots of brown should be perfect in representing the treehouse experience in simple colour.

- The fonts chosen from google fonts for the header "treeHouse" are -blank- and Bonheur Royale. These are characteristic of the strong tree trunk and the elegant branches of leaves. This combination also could evoke the image of a treehouse.

- I used icons from font-awesome for relevant inputs, navigation and dropdown menu. For the "add to favourites" button I used a heart symbol, the obvious choice and emblematic of a like button.

## Features

### Landing Page

- This is a static page which features everything the user needs to navigate the site and understand it's purpose. The message "HELP US CLEAN UP THE PLANET WHILE KEEPING YOU AND YOUR HOME CLEAN" lets the user know the mission of the site. It also points directly to the kind of products for sale without requiring the user to read a paragraph or two about the aim of the e-commerce shop.
- The large "Shop Now" button immediately below the message is ideally placed below the question to suggest to the user the best way they can help us clean up the planet.
- The Blog button gives them an option to become more informed about the mission of the site and the stories of people leading eco-lives.
- The message below the header tells the user that they can get free delivery with a purchase over €40. A welcome message which doesn't obtrude on the page greatly.
- The header contains a search bar, the title and a couple of icons for navigation. One of the icons is a person indicating personal/user info, it triggers a dropdown menu with links relating to the user's profile. The other icon is a link to the shopping cart and also displays a running total of it's contents beneath it.
- There is a bottom section to the header which displays dropdown links for the range of products and one for the csategories for the user to easily navigate to their preferred products from the homepage.

### Products Page

- The products page extends the base template and features a "sort by" selecter and gives the user the number of products displayed by the given search or category.
- Products can be sorted by price, category, or alphabetically.
- If a category has been selected the category is diplayed below the "Products" heading.
- The products are displayed in rows of 4, 3, 2, or 1 depending on the width of the page, from large to small.
- The images are capped at a max height so that they don't stand out too much in their row given the different image shapes that could be uploaded.
- Beneath the image is the name of the product, the price and the category that it's in.
- If the user clicks on the category below they will be presented with all products of that category.
- There is a heart icon to the bottom left of the product that the user can click to add the product to their favourites list.
- As the user scrolls down the page through the products the bottom part of the header and the free delivery announcment slide out of view to give them a better view of the products.
- The header is also transparent so it doesn't impare the view more than it needs to while remaining clear if the user does wish to use it.

#### Product Detail Page

  - This page displays a larger image of the product with some information about it and a review in stars out of 5.
  - The product can be added to the users shopping basket from here with an "add to cart" button.
  - There is quantity selector so the user can choose how many of the product they wish to add.
  - The heart icon is also on this page so it can be added to favourites from here also.

### Shopping Bag Page

- When the user has finished shopping they can click the icon in the top left corner and be brought to the bag page.
- This page allows the user to look at the products they have in their cart and edit them.
- There is a quantity selector next to the products for the user to add to or reduce the number of an item. They would then click the update button below to register the change.
- A remove button allows them to remove a product immediately if they wish.
- The price for each item is displayed to the side and a total is displayed at the bottom with a message letting them know how far from a free delivery they are if the total is less than €40.
- The checkout now button is just below, directing straight to a payments page.
- When a product has been added to the cart it will trigger a dropdown displaying the contents of the bag, the toal price and a link to go directly to checkout.

### The Checkout Page

- If not logged in, the user will be required to give their 
