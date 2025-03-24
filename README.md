# Gemini Testing for AI in Fashion

This document showcases the testing of Gemini, an AI tool, for various fashion-related use cases. The goal is to demonstrate how AI can enhance and transform fashion imagery, including outfit generation, background changes, product placement, and 3D modeling. These tests are intended to be presented to product owners in a corporate setting to highlight the potential of AI in the fashion industry.

---




## Case #1: Put Clothes on the Model  
**Objective:** Dress the model in specified clothing items while maintaining realism, professional style, and the original silhouette. The background and model's face should remain unchanged.


```python
$ python app.py --text "Put these jeans and shirt on the model, make it super realistic and keep the professional style, keep the model in the same silhouette, don't change the background and model's face" --files model.jpeg jeans.jpeg shirt.jpeg
```

## Input

| ![Jeans](https://i.postimg.cc/Zn24sB9m/jeans.jpg) | ![Model](https://i.postimg.cc/pV6WL7sS/model.jpg) | ![Shirt](https://i.postimg.cc/nc9Hjk5h/shirt.jpg) |
|---------------------------------------------------|--------------------------------------------------|--------------------------------------------------|

## Output

![](https://i.postimg.cc/wM79kcjF/ai-dhy4igla.png
)

## Case #2: Background Change

**Objective**: Modify the background of the model's image to a vibrant forest scene with a sunrise.

```python
$ python app.py --text "Change background to forest, sunrise, vibrant" --files model2.jpeg 
```

## Input

![](https://i.postimg.cc/3NBcfWtR/model2.jpg)


## Output

![](https://i.postimg.cc/zBTMWxWT/ai-13d-cldn.png))

## Case #3 Place fashion products

**Objective**: Add accessories (sunglasses and a hat) to the model's outfit.

```python
$ python app.py --text "Put sunglasses and hat on the model" --files model2.jpeg 
```

## Input

![](https://i.postimg.cc/3NBcfWtR/model2.jpg)

## Output

![](https://i.postimg.cc/NFZ5V8pG/ai-v1k1nvfn.png)

## Case #4: Change model's face

**Objective**: Alter the model's face to an Asian appearance and change the hair color to blue.

```python
$ python app.py --text "Change model face's to asian and color hair's to blue" --files model2.jpeg
```

## Input

![](https://i.postimg.cc/3NBcfWtR/model2.jpg)

## Output

![](https://i.postimg.cc/RZNfVRWR/ai-2ncw9iqc.png)

## Case #5: Change Clothing Color

**Objective**: Modify the color of the model's t-shirt to a specific hex color (#8a00e6).

```python
$ python app.py --text "Change t-shirt color to #8a00e6" --files model3.jpeg  
```

## Input

![](https://i.postimg.cc/HkF95K5n/model3.jpg)

## Output

![](https://i.postimg.cc/MTS03Q98/ai-lon5kn1d.png)

## Case 6: Put object on the clothing

**Objective**: Add a Gandalf logo to the model's t-shirt.

```python
$ python app.py --text "Put face gandalf logo on the t-shirt" --files model3.jpeg  
```

## Input

![](https://i.postimg.cc/HkF95K5n/model3.jpg)

## Output

![](https://i.postimg.cc/vTcNbKVs/ai-k7fd9gnn.png)

## Case 7: 3D Object Creation

**Objective**: Transform a 2D image of jeans into a high-quality 3D model for use in an online store. The 3D model should showcase realistic textures, folds, and shading, allowing customers to view the product from multiple angles.

```python
$ python app.py --text "I have a product image of jeans, and I need to transform it into a high-quality 3D model for use in an online store. The 3D model should be realistic, with accurate textures, folds, and shading to showcase the jeans in a visually appealing way. The goal is to make the jeans look as lifelike as possible, so customers can view them from multiple angles (front, back, side) and get a clear understanding of the product's design ." --files jeans.jpeg     
```

## Input

![Jeans](https://i.postimg.cc/Zn24sB9m/jeans.jpg)

## Output

![](https://i.postimg.cc/zBsHdb81/ai-xd38hpdc.png)

## Case #8: Generate description and hashtags

**Objective**: Generate catchy description and hashtags of the product.


```python
$ python app.py --text "Generate product description and hashtags for online shopping website, make it super energetic, captivating and catchy, we want to user's to but this product" --files shirt.jpeg

```

## Input

![Shirt](https://i.postimg.cc/nc9Hjk5h/shirt.jpg)

## Output


Unleash Your Inner Wildcat!

Ready to ROAR with style? 

This isn't just a top; it's a statement! 

Slip into this fierce leopard print and watch heads turn. The purr-fect blend of comfort and bold design, it's guaranteed to elevate your everyday look from drab to **DRAMA!** Whether you're hitting the city streets or just want to add some spice to your Zoom calls, this top is your secret weapon for instant confidence. Don't just follow the trends, **lead the pack!** Grab yours now before it's gone!

#LeopardLove #WildStyle #FierceFashion #MustHave #AddToCart




