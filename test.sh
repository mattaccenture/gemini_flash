#!/bin/zsh


MODEL="Generate a high-fashion model wearing the exact clothing items from the provided reference images. Show the model in a full-body pose that clearly displays all garment details. Requirements: 1) Perfectly replicate the clothing items' cuts, patterns, textures, and draping from references, 2) Maintain realistic fabric behavior (folds, movement), 3) Use a neutral pose that highlights the clothing, 4) Keep the background simple (white studio or subtle gradient). Ensure all clothing details (stitching, prints, accessories) match the reference images exactly, with photorealistic quality and proper fit on the model's body."

FABRIC="Design a summer dress based on this fabric, elegant, vibrant." 

BACKGROUND="Change the background while perfectly preserving the original ground surface where the model stands - maintain the exact floor texture (white marble runway), perspective, shadows beneath feet, and lighting conditions. Only replace the upper background with futuristic cyberpunk cityscape at night. Keep all glossy runway reflections."

SKETCH="Reference sketch to generate: A breathtaking modern haute couture opera gown, translating the sketch design faithfully. Elegant, dramatic silhouette, flowing luxurious fabric (velvet or heavy silk suggested). Setting: Opera stage, dramatic spotlight, cinematic lighting. Quality: Photorealistic, highly detailed, fashion magazine style, 8K, full body shot."

FACE_CHANGE="Inpaint a photorealistic face of a young korean man. Blend seamlessly with the surrounding skin tone, hair, and neck. Match the original photo's lighting, style, and resolution precisely. High detail."

COMBINE="Generate a uniform inspired by the provided three reference images, combining their best elements into a single design"



#python img --prompt $BACKGROUND --files model7.jpeg --output $PWD/test/cases/background1.png 
#python img --prompt $CLOTHING  --files basic1.jpeg basic2.jpeg basic3.jpeg --output $PWD/test/cases/clothing.png 
#python img --prompt $FABRIC --files fabric.png --output $PWD/test/cases/fabric_dress.png 
#python img --prompt $SKETCH --files sketch.jpg  --output $PWD/test/cases/test.png
python img --prompt $FACE_CHANGE --files model3.jpeg  --output $PWD/test/cases/face_change.png

#python img --prompt $COMBINE --files model7.jpeg model13.jpeg  --output $PWD/test/cases/combine.png
