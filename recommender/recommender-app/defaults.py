from repository.models import Product, Review

product1 = Product()
product1.title='Product1'
product1.description='Product1 description'
product1.asin='Product1 asin'
product1.imUrl='https://boxboysupplies.com/wp-content/uploads/2018/04/boxed-inn-12x9x6-shipping-box.jpg'
product1.brand='Product1 brand'
product1.categories='Product1 categories'
product1.price=10
product1.related='Product1 related'
product1.salesRank='Product1 sales rank'

review1 = Review()
review1.asin='Review1 asin'
review1.reviewerID='Review1 reviewerId'
review1.product_id='Review1 productId'
review1.helpful=2
review1.id='Review1 id'
review1.overall=3
review1.reviewerName='Review1 reviewerName'
review1.reviewText='Review1 reviewText'
review1.unixReviewTime='Review1 unixReviewTime'
review1.summary='Review1 summary'

ad1 = Product()
ad1.title='Ad1'
ad1.description='Ad1 description'
ad1.asin='Ad1 asin'
ad1.imUrl='https://fiverr-res.cloudinary.com/t_main1,q_auto,f_auto/gigs/119950745/original/48df3716297fea4f964b005e560fe0135a1f5182.jpeg'
ad1.brand='Ad1 brand'
ad1.categories='Ad1 categories'
ad1.price=10
ad1.related='Ad1 related'
ad1.salesRank='Ad1 sales rank'


default_products = [product1]
default_reviews = [review1]
default_ads = [ad1]