-- SQLite database dump
PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE ai_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
INSERT INTO "ai_messages" VALUES(1,'web-mbye29rg5ba','user','111','2025-08-28T03:40:52.946745');
INSERT INTO "ai_messages" VALUES(2,'web-mbye29rg5ba','assistant','问题已收到：111
依据已知生物学常识进行概括：请聚焦关键概念与因果机制。（示例回答，可在后端接入真实模型）','2025-08-28T03:40:52.958758');
INSERT INTO "ai_messages" VALUES(3,'web-mbye29rg5ba','user','解释ATP','2025-08-28T03:41:14.730307');
INSERT INTO "ai_messages" VALUES(4,'web-mbye29rg5ba','assistant','问题已收到：解释ATP
依据已知生物学常识进行概括：请聚焦关键概念与因果机制。（示例回答，可在后端接入真实模型）','2025-08-28T03:41:14.738483');
INSERT INTO "ai_messages" VALUES(5,'web-dvlwn40wd2n','user','生物酶的概念','2025-08-28T06:31:24.406102');
INSERT INTO "ai_messages" VALUES(6,'web-dvlwn40wd2n','assistant','生物酶，也称为酶（Enzymes），是一类具有生物催化作用的蛋白质。以下是关于生物酶的关键概念和因果机制的条理清晰概述：

1. **生物催化作用**：
   - 酶的主要功能是加速生物体内的化学反应，它们能够显著降低反应所需的活化能，从而提高反应速率。

2. **蛋白质组成**：
   - 几乎所有酶都是由蛋白质构成，极少数酶（如核酸酶）是由核酸构成。

3. **特异性**：
   - 酶对底物（即它们催化的反应物）具有高度的特异性。一种酶通常只能催化一类或几种特定的底物。

4. **活性中心**：
   - 酶分子中有一个特定的区域，称为活性中心，底物在这里与酶结合并发生反应。

5. **动态结构**：
   - 酶分子具有一定的动态性，其结构在底物结合时发生变化，以实现催化功能。

6. **非永久性改变**：
   - 在催化反应过程中，酶分子不会被消耗或发生永久性改变，它们可以反复使用。

7. **作用机制**：
   - 酶降低反应的活化能，提高反应速率，但并不改变反应的平衡状态。

8. **环境敏感性**：
   - 酶的活性受到环境因素的影响，如温度、pH值等，这些因素可以影响酶的活性中心结构，进而影响其催化能力。

9. **调控作用**：
   - 生物体内的酶活性可以通过多种方式进行调控，如通过激素、基因表达调控等，从而精确控制生物体内的代谢过程。

10. **合作与竞争性抑制**：
    - 酶活性可以被特定化合物（如激活剂）增强，也可以被其他化合物（如抑制剂）降低或抑制。

11. **酶的分类**：
    - 根据催化反应的类型，酶可以分为六大类：氧化还原酶、转移酶、水解酶、裂合酶、异构酶和连接酶。

了解这些关键概念有助于深入理解酶在生物体内的作用和重要性。','2025-08-28T06:31:24.414121');
INSERT INTO "ai_messages" VALUES(7,'web-7gpu0si8k4h','user','ATP','2025-08-28T06:42:36.107543');
INSERT INTO "ai_messages" VALUES(8,'web-7gpu0si8k4h','assistant','ATP（三磷酸腺苷）是细胞能量代谢的核心分子，直接参与细胞内各种能量需求过程。以下是关于ATP的关键概念和因果机制的简明回答：

1. **定义**：
   ATP是细胞内的一种高能分子化合物，化学式为C10H16N5O13P3，由一个腺嘌呤（Adenine）、一个核糖（Ribose）和三个磷酸基团（Phosphate）组成。

2. **结构特点**：
   - **高能磷酸键**：ATP分子中的“高能磷酸键”指的是远离腺嘌呤的两个磷酸基团之间的化学键，这种化学键具有较高的化学势能，能够快速释放能量。
   - **稳定性**：高能磷酸键相对不稳定，在水解时会释放大量能量，供应细胞进行各种生命活动。

3. **能量转移**：
   - **ATP合成**：细胞通过呼吸作用或光合作用将化学能转化为ATP中的化学能，通常涉及电子传递链和化学磷酸化作用。
   - **ATP水解**：细胞在需要能量时，ATP的水解会释放能量，将一个磷酸基团转化为ADP（二磷酸腺苷）和无机磷酸（Pi）。

4. **功能**：
   - **供能**：ATP是细胞能量的主要来源，为细胞内各种代谢反应提供所需的能量。
   - **信号传递**：ATP也参与细胞信号传递过程，如肌肉收缩和神经传递。

5. **能量转换**：
   - **ATP循环**：细胞内ATP、ADP和AMP（一磷酸腺苷）之间的转换是一个动态平衡过程，被称为ATP-ADP循环或能量循环。

6. **能量储存**：
   - **ATP的储存量有限**：细胞内ATP的储存量相对较少，但ATP的合成和分解速度非常快。

7. **能量效率**：
   - **能量利用效率**：ATP水解时释放的能量效率非常高，大约有30-40%的能量被用于细胞工作，其余以热能形式散失。

综上所述，ATP是细胞活动能量转换的关键分子，通过ATP-ADP循环实现能量的快速供应和储存，是细胞生命活动不可或缺的组成部分。','2025-08-28T06:42:36.116545');
INSERT INTO "ai_messages" VALUES(9,'web-av2b9mu1ru8','user','ATP','2025-08-28T06:56:54.044325');
INSERT INTO "ai_messages" VALUES(10,'web-av2b9mu1ru8','assistant','ATP（三磷酸腺苷）是细胞能量储存和转移的关键分子。以下是关于ATP的一些关键概念和因果机制：

1. **结构组成**：
   - ATP由一个腺苷分子和三个磷酸基团组成。
   - 分子式为C10H16N5O13P3。

2. **功能**：
   - ATP是细胞内大多数能量需求过程的直接能量来源。
   - 它通过水解反应释放能量，形成ADP（二磷酸腺苷）和无机磷酸盐（Pi）。

3. **能量储存**：
   - ATP中的高能磷酸键，特别是最末端的磷酸键，储存了大量的化学能。
   - 这些能量在细胞需要时被释放，例如肌肉收缩、细胞分裂和跨膜运输等。

4. **能量转移的机制**：
   - 在ATP水解过程中，ATP分子通过磷酸键断裂释放能量。
   - 这个过程中，一个磷酸基团被移除，形成ADP和无机磷酸盐。
   - 这个过程是可逆的，即ADP和无机磷酸盐可以重新结合，形成ATP，这个过程通常需要来自呼吸作用或光合作用的能量。

5. **能量的转换**：
   - ATP水解释放的能量被用来驱动许多细胞过程，包括合成代谢反应和肌肉收缩。
   - 在合成代谢反应中，ATP提供所需的能量来合成新的分子，如蛋白质、脂肪和核酸。

6. **细胞内浓度与再生**：
   - 细胞内ATP的浓度相对较低，但由于其快速再生，可以满足细胞的能量需求。
   - ATP的再生依赖于细胞的代谢活动，例如糖酵解、柠檬酸循环和氧化磷酸化。

7. **酶的作用**：
   - 多种酶参与ATP的合成和水解过程，例如ATP合酶和ATP水解酶。
   - 这些酶确保ATP的合成和水解过程高效、可调，并能够迅速响应细胞的能量需求。

总结来说，ATP是细胞内能量转移的核心分子，通过其与ADP之间的快速循环，细胞能够维持必要的能量供应。ATP的结构特点使其能够储存和释放大量能量，支持细胞的各种生命活动。','2025-08-28T06:56:54.052626');
INSERT INTO "ai_messages" VALUES(11,'web-yzear80mkfi','user','ATP','2025-08-28T06:57:13.654643');
INSERT INTO "ai_messages" VALUES(12,'web-yzear80mkfi','assistant','ATP，全称三磷酸腺苷（Adenosine Triphosphate），是生物体内能量转移和储存的主要分子。以下是关于ATP的关键概念和因果机制：

1. **结构组成**：
   - **腺苷**：由腺嘌呤（一个含氮碱基）和核糖（五碳糖）组成的部分。
   - **磷酸基团**：三个磷酸基团（PO4^3-）通过高能磷酸键连接在核糖上。

2. **能量转移**：
   - ATP中的能量主要储存在高能磷酸键中，特别是远离腺苷的两个磷酸键中。这些键被称为α磷酸键和β磷酸键。
   - 当ATP水解时，一个磷酸基团被移除，转化为ADP（二磷酸腺苷）和无机磷酸（Pi），释放出能量。

3. **能量储存与释放**：
   - ATP作为能量货币，其合成和分解反应是细胞内能量代谢的核心。
   - **合成**：ATP合成通常发生在细胞的线粒体或叶绿体中，能量来源于呼吸作用或光合作用。
   - **分解**：在需要能量的生物过程中，ATP被分解为ADP，释放出能量以供细胞使用。

4. **细胞功能**：
   - ATP是细胞内许多生物化学反应的直接能量来源，包括肌肉收缩、细胞分裂、蛋白质合成等。

5. **合成途径**：
   - **直接合成**：通过磷酸化反应，如磷酸肌酸（PCr）和ATP之间的相互转化。
   - **间接合成**：通过代谢途径，如糖酵解、三羧酸循环（TCA循环）和氧化磷酸化过程产生ATP。

6. **ATP维持**：
   - 细胞中ATP的浓度并不高，但ATP和ADP之间的快速转化使得细胞能够快速响应能量需求的变化。

7. **ATP的循环**：
   - ATP和ADP之间的转化是细胞内能量代谢的循环过程，这个循环确保细胞能够持续供应能量。

8. **能量效率**：
   - ATP水解时释放的能量效率很高，大部分能量可以直接用于生物化学反应，只有少量能量以热的形式散失。

以上是ATP的基本介绍和其在生物学中的关键作用。ATP的合成和分解是细胞能量代谢的基础，对于维持细胞的生理活动至关重要。','2025-08-28T06:57:13.665206');
INSERT INTO "ai_messages" VALUES(13,'web-2jkri456ck3','user','ATP','2025-08-28T07:09:05.324441');
INSERT INTO "ai_messages" VALUES(14,'web-2jkri456ck3','assistant','ATP（三磷酸腺苷，Adenosine triphosphate）是一种在细胞中广泛存在的高能化合物，它是细胞能量传递和储存的主要分子。以下是关于ATP的关键概念和因果机制：

1. 结构特点：
   - ATP由腺嘌呤（Adenine）、核糖（Ribose）和三个磷酸基团（Phosphate groups）组成。
   - 磷酸基团通过高能磷酸键连接，最外端的键称为末端高能磷酸键，它是ATP能量的主要来源。

2. 功能：
   - ATP作为细胞的直接能量来源，参与细胞内许多生命活动，如肌肉收缩、细胞分裂、代谢过程等。
   - ATP通过水解反应释放能量，转化为ADP（二磷酸腺苷）和无机磷酸（Pi）。

3. 能量转换：
   - ATP与ADP之间的转化是细胞能量转换的关键过程。
   - ATP生成：通过光合作用和细胞呼吸等过程，将光能或化学能转化为ATP中的化学能。
   - ATP水解：ATP提供能量，通过水解生成ADP和Pi，释放能量供细胞活动使用。

4. 能量储存：
   - ATP的储存量相对较少，但转化效率高，能迅速提供能量。
   - 细胞中ATP与ADP的浓度比是调节能量代谢的重要参数。

5. 能量供应的连续性：
   - ATP的生成和水解是一个动态平衡过程，确保细胞在不同状态下的能量供应。
   - 通过各种代谢途径，细胞能够连续不断地合成ATP，以维持生命活动。

总结来说，ATP是细胞内能量转换和储存的关键分子，其结构特点使其能够快速释放和储存能量，支持细胞的各项生命活动。ATP与ADP之间的动态转化是细胞能量供应的基石，确保了细胞能量代谢的连续性和有效性。','2025-08-28T07:09:05.333154');
INSERT INTO "ai_messages" VALUES(15,'web-rmmabftsd8','user','ATP','2025-08-28T07:13:02.264389');
INSERT INTO "ai_messages" VALUES(16,'web-rmmabftsd8','assistant','ATP（三磷酸腺苷）是细胞能量代谢中的核心分子，以下是对其关键概念和因果机制的简练且条理清晰的解释：

1. **定义**：
   - ATP是由腺苷和三个磷酸基团组成的分子，其结构可以表示为A-P~P~P，其中A代表腺苷，P代表磷酸基团，而波浪线表示高能磷酸键。

2. **功能**：
   - **能量载体**：ATP是细胞内大多数能量需求过程的直接能量来源。它通过水解释放能量，用于各项生命活动。
   - **能量转移**：在代谢过程中，能量通过磷酸基团的转移从一种分子转移到另一种分子。

3. **能量储存与释放**：
   - **高能磷酸键**：ATP分子中的高能磷酸键（尤其是远离腺苷的β-γ键）储存了大量的化学能。
   - **水解释放能量**：当ATP水解成ADP（二磷酸腺苷）和无机磷酸（Pi）时，储存在高能磷酸键中的能量被释放出来，供细胞使用。

4. **ATP合成**：
   - **氧化磷酸化**：在细胞呼吸过程中，电子传递链通过氧化磷酸化过程生成ATP。
   - **光磷酸化**：在光合作用的光反应阶段，光能被转化为化学能，产生ATP。

5. **ATP与ADP的循环**：
   - **ATP生成**：细胞通过各种代谢途径（如糖酵解、三羧酸循环、氧化磷酸化）生成ATP。
   - **ATP消耗**：ATP被细胞的各种活动（如肌肉收缩、合成代谢、主动运输）消耗，转化为ADP。
   - **ATP再合成**：ADP通过上述代谢途径再次转化为ATP，形成ATP-ADP循环。

6. **ATP的调控**：
   - **ATP合成与消耗的平衡**：细胞必须维持ATP的合成和消耗之间的平衡，以保持能量供应与需求的平衡。

7. **ATP的重要性**：
   - **生命活动的基础**：ATP是所有细胞生命活动的基础，没有ATP，细胞将无法进行大多数代谢过程。

综上所述，ATP是细胞内能量转换和储存的关键分子，通过其合成和分解过程，细胞能够调节能量供应，以满足不同生命活动的需求。','2025-08-28T07:13:02.272340');
INSERT INTO "ai_messages" VALUES(17,'web-erz6tvbw2l5','user','光合作用过程','2025-08-28T07:35:11.476628');
INSERT INTO "ai_messages" VALUES(18,'web-erz6tvbw2l5','assistant','光合作用是植物、藻类和某些细菌利用光能将二氧化碳和水转化为有机物（主要是葡萄糖）和氧气的过程。以下是光合作用过程的简练表述，分为光反应和暗反应两个阶段：

1. **光反应阶段（发生在叶绿体的类囊体膜上）**：
   - 光能吸收：叶绿素和其他色素吸收光能。
   - 水的光解：水分子在光能的作用下被分解成氧气和氢离子。
   - ATP合成：氢离子通过电子传递链产生ATP（三磷酸腺苷），同时产生NADPH（还原型烟酰胺腺嘌呤二核苷酸磷酸）。

2. **暗反应阶段（发生在叶绿体的基质中）**：
   - 二氧化碳固定：二氧化碳被固定到一个五碳糖上，形成两个三碳化合物（C3）。
   - 二氧化碳还原：ATP和NADPH提供能量和还原力，将C3化合物还原成糖类等有机物。
   - 再生五碳糖：通过一系列的酶促反应，部分C3化合物被转化为五碳糖，用于新一轮的二氧化碳固定。

关键概念与因果机制：
- **光能转换**：光合作用首先是光能转换为化学能的过程，其中光能通过光合色素被捕捉并转化为电子的能量状态。
- **水的光解**：光反应中，水分子的光解产生氧气，是光合作用中产生氧气的直接原因。
- **ATP和NADPH的生成**：光反应通过电子传递链和光磷酸化作用产生ATP和NADPH，为暗反应提供能量和还原力。
- **二氧化碳固定**：暗反应中，二氧化碳被固定到有机物中，这是光合作用中有机物合成的起点。
- **碳循环**：暗反应中的卡尔文循环是二氧化碳还原的主要过程，通过这个循环，二氧化碳被转化为有机物，同时再生五碳糖以维持循环。

光合作用是地球上最重要的生物化学过程之一，它不仅为植物自身提供能量和生长所需的物质，同时也是地球上氧气的主要来源，对生态系统和大气组成有着深远的影响。','2025-08-28T07:35:11.485642');
INSERT INTO "ai_messages" VALUES(19,'web-bkdmo0qletd','user','ATP的过程','2025-08-28T08:33:23.079127');
INSERT INTO "ai_messages" VALUES(20,'web-bkdmo0qletd','assistant','ATP（腺苷三磷酸）是细胞内能量转移的关键分子，参与了细胞中几乎所有的能量需求过程。ATP的生成和消耗是通过以下两个主要过程来实现的：

1. **ATP的合成过程：**
   - **光合作用：** 在植物的叶绿体中，通过光合作用可以合成ATP。光能被叶绿素吸收后，激发电子，通过一系列电子传递链产生质子梯度，最终通过ATP合成酶合成ATP。
   - **呼吸作用：** 在细胞的线粒体中进行，通过氧化磷酸化合成ATP。氧气作为最终电子受体参与电子传递链，产生质子梯度，驱动ATP合成酶合成ATP。
   - **底物磷酸化：** 某些代谢途径中，底物分子直接将磷酸团转移给ADP形成ATP。

2. **ATP的水解过程：**
   - **ATP水解释放能量：** ATP在消耗时，通过水解反应释放出储存的能量。当细胞需要能量时，ATP分子中的高能磷酸键断裂，释放能量供细胞使用。水解后，ATP转化为ADP（腺苷二磷酸）和无机磷酸（Pi）。
   - **能量转移：** ATP的水解使能量从一个反应转移到另一个反应。例如，在肌肉收缩时，ATP水解释放的能量被用来推动肌动蛋白和肌球蛋白的相互作用，导致肌肉纤维缩短。
   - **细胞内其他过程：** 细胞内许多生物合成反应和转运过程都需要ATP提供能量。

总结来说，ATP的合成和水解过程是细胞能量转换的核心，涉及到光合作用、呼吸作用以及底物磷酸化。ATP的合成是通过质子梯度驱动的，而水解则通过释放能量来支持细胞的各种活动。这种循环机制确保了细胞能够持续地获取和利用能量。','2025-08-28T08:33:23.087631');
INSERT INTO "ai_messages" VALUES(21,'web-xarrk0a0yhk','user','光合作用介绍','2025-08-28T08:44:23.654642');
INSERT INTO "ai_messages" VALUES(22,'web-xarrk0a0yhk','assistant','光合作用是绿色植物在叶绿体中利用光能将二氧化碳和水转化为有机物，并释放氧气的过程，同时将光能转化成化学能储存在合成的有机物中。以下是光合作用的关键概念和因果机制：

1. **光合作用的场所：** 主要发生在植物的叶绿体中。

2. **光合作用的基本反应：**
   \[
   \text{二氧化碳} + \text{水} \xrightarrow{\text{光能}} \text{有机物（储存能量）} + \text{氧气}
   \]

3. **光合作用的两个阶段：**
   - **光反应（光依赖阶段）：** 发生在叶绿体的类囊体膜上，需要光能。光能被叶绿素吸收后，用于水的光解产生氧气、[H]（还原氢）和ATP。
   - **暗反应（光合作用中的暗反应）：** 发生在叶绿体的基质中，不需要光，是二氧化碳固定和还原的过程。利用ATP和[H]将二氧化碳还原成有机物。

4. **光合作用的关键概念：**
   - **光能的吸收与转换：** 光能被叶绿素分子吸收，并转化为化学能。
   - **光解水：** 在光反应中，水分子被光解为氧气和电子。
   - **ATP的生成：** 光反应过程中，电子通过电子传递链产生ATP。
   - **[H]的生成：** 光解水产生的电子和质子（H+）结合形成[H]，用于暗反应。
   - **CO2的固定：** 在暗反应中，CO2被固定为三碳化合物。
   - **CO2的还原：** [H]和ATP提供能量和还原力，将三碳化合物还原为有机物。

5. **光合作用的因果机制：**
   - **光能的利用：** 光合作用开始于光能的吸收，这是整个过程的能量来源。
   - **水的光解：** 光能触发水分子的光解，产生氧气和电子。
   - **ATP和NADPH的产生：** 电子通过电子传递链产生ATP和NADPH（另一种含能量的分子）。
   - **暗反应的进行：** ATP和NADPH在暗反应中提供能量，将CO2转化为有机物。
   - **有机物的合成：** 最终，CO2被转化为葡萄糖等有机物，储存了光合作用中固定的化学能。

光合作用不仅为植物自身提供了生长所需的有机物和能量，也是地球上氧气的主要来源，对于维持生态系统的平衡和支持其他生物的生存至关重要。','2025-08-28T08:44:23.663799');
INSERT INTO "ai_messages" VALUES(23,'web-gobkpkvg8d','user','你好','2025-08-28T08:46:57.503983');
INSERT INTO "ai_messages" VALUES(24,'web-gobkpkvg8d','assistant','你好！请问有什么生物学问题我可以帮你解答吗？我会尽力提供准确、简练、条理清晰的答案，并强调关键概念与因果机制。请随时提问。','2025-08-28T08:46:57.512046');
INSERT INTO "ai_messages" VALUES(25,'web-n87n60euswd','user','光合作用','2025-08-28T08:48:20.432491');
INSERT INTO "ai_messages" VALUES(26,'web-n87n60euswd','assistant','光合作用是绿色植物通过叶绿体利用光能将二氧化碳和水转化为储存能量的有机物（主要是淀粉），并释放氧气的过程。以下是光合作用的各个关键概念和因果机制：

1. **光合作用的场所**：
   - **叶绿体**：植物细胞中的一种细胞器，含有叶绿素，是光合作用的主要场所。

2. **光合作用的原料**：
   - **二氧化碳（CO₂）**：植物通过气孔吸收空气中的二氧化碳。
   - **水（H₂O）**：植物通过根部从土壤中吸收水分。

3. **光合作用的产物**：
   - **有机物（如淀粉）**：储存光合作用固定的能量。
   - **氧气（O₂）**：作为光合作用的副产品释放到大气中。

4. **光合作用的类型**：
   - **光反应（光依赖反应）**：在叶绿体的类囊体膜上进行，利用光能将水分解为氧气和氢离子，同时产生ATP和NADPH。
   - **暗反应（光合作用的暗反应或Calvin循环）**：在叶绿体的基质中进行，利用ATP和NADPH将二氧化碳转化为有机物。

5. **光合作用的过程**：
   - **光反应**：
     - **光能的捕获**：叶绿素和其他色素吸收光能。
     - **水的光解**：水分子被分解为氧气、电子和氢离子。
     - **ATP和NADPH的生成**：电子通过电子传递链，能量被用来合成ATP和NADPH。
   - **暗反应**：
     - **CO₂的固定**：CO₂与五碳糖（RuBP）结合，形成两个三碳糖（3-PGA）。
     - **三碳糖的还原**：3-PGA被ATP和NADPH还原成有机物质，如葡萄糖。

6. **光合作用的意义**：
   - **能量转换**：将光能转换为化学能，储存在有机物中。
   - **物质转化**：将简单的无机物转化为复杂的有机物。
   - **生态平衡**：为生物圈提供食物和氧气，维持生物圈的碳-氧平衡。

7. **影响光合作用的因素**：
   - **光照强度**：影响光反应的速率。
   - **温度**：影响酶的活性，进而影响暗反应。
   - **二氧化碳浓度**：影响暗反应的速率。
   - **水分**：影响植物的生长和光合作用的进行。

光合作用是地球上生命存在的基础，它不仅为植物自身提供能量和生长所需的有机物，还为其他生物提供了食物和氧气，是生态系统中能量流动和物质循环的核心过程。','2025-08-28T08:48:20.441504');
INSERT INTO "ai_messages" VALUES(27,'web-sj47fx8ewfb','user','光合作用过程','2025-08-28T08:55:25.946861');
INSERT INTO "ai_messages" VALUES(28,'web-sj47fx8ewfb','assistant','光合作用是植物、藻类和某些细菌利用光能将二氧化碳和水转化为有机物质（如葡萄糖）和氧气的过程。以下是光合作用的简要概述，分为两个阶段：光反应和暗反应（也称为光合作用的光依赖反应和光独立反应）。

1. **光反应（发生在叶绿体的类囊体膜上）**：
   - **光能吸收**：叶绿素等色素吸收光能。
   - **水的光解**：水分子在光能的作用下被分解为氧气、电子和氢离子（H+）。
   - **ATP和NADPH的生成**：
     - 电子通过电子传递链传递，释放能量，用于合成ATP（三磷酸腺苷）。
     - 氢离子在类囊体膜内外形成浓度梯度，通过ATP合酶生成ATP。
     - 同时，氢离子和电子也被用来将NADP+（烟酰胺腺嘌呤二核苷酸磷酸）还原成NADPH。

2. **暗反应（发生在叶绿体的基质中，但不需要光照）**：
   - **二氧化碳的固定**：通过Calvin循环（也称为C3途径），二氧化碳被固定到一个5碳糖分子（RuBP，核糖二磷酸）上，生成一个不稳定的6碳中间产物。
   - **二氧化碳的还原**：6碳中间产物分裂成两个3碳分子（PGA，磷酸丙酮酸）。
   - **有机物质的合成**：
     - PGA被还原成G3P（甘油醛-3-磷酸），其中一些G3P分子形成葡萄糖或其他有机物质。
     - 其余的G3P分子重新生成RuBP，完成Calvin循环，以便继续固定更多的二氧化碳。

**关键概念与因果机制**：
- **光能转换**：光合作用始于光能的捕获和转换为化学能，这是通过光反应中的水分解实现的。
- **ATP和NADPH的作用**：这两个分子是光合作用中产生的高能化合物，它们在暗反应中提供能量和还原力，用于固定和还原二氧化碳。
- **Calvin循环**：这是暗反应中的循环过程，负责将ATP和NADPH的能量用于合成有机物质，特别是葡萄糖。
- **氧气的释放**：作为光反应的副产品，氧气被释放到大气中，这是地球上氧气的主要来源。

光合作用是地球上生命维持的关键过程，它不仅为植物自身提供能量和生长所需的物质，还为其他生物提供食物和氧气。','2025-08-28T08:55:25.955754');
INSERT INTO "ai_messages" VALUES(29,'web-yfmjk3y37br','user','光合作用过程','2025-08-28T08:58:20.141185');
INSERT INTO "ai_messages" VALUES(30,'web-yfmjk3y37br','assistant','光合作用是植物、藻类和某些细菌将光能转化为化学能的过程，主要分为光反应和暗反应（也称为光依赖性反应和光合作用的光独立阶段）。以下是光合作用的简练、条理清晰的解释：

1. **光反应**：
   - **场所**：叶绿体的类囊体膜。
   - **关键色素**：叶绿素。
   - **能量转换**：叶绿素吸收光能，激发电子到更高的能级。
   - **水的光解**：激发的电子用于将水分子分解成氧气、质子和电子。
   - **ATP和NADPH的产生**：
     - **ATP的合成**：质子通过ATP合成酶梯度驱动形成ATP。
     - **NADPH的合成**：电子通过电子传递链最终传递给NADP+，形成NADPH。
   - **氧气释放**：作为副产品释放到大气中。

2. **暗反应**（Calvin循环）：
   - **场所**：叶绿体的基质。
   - **二氧化碳固定**：二氧化碳与一个5碳糖（RuBP）结合生成两个3碳化合物（3-PGA）。
   - **还原反应**：利用ATP提供的能量和NADPH提供的还原力，3-PGA被还原成G3P。
   - **再生和糖类合成**：
     - 一部分G3P被转化为糖类（如葡萄糖）储存能量。
     - 其余G3P用于再生RuBP，以便循环的继续。

**关键概念与因果机制**：
- **光能的吸收**：叶绿素吸收特定波长的光能，这是光合作用的起始步骤。
- **光依赖性反应**：光能转化为化学能，产生氧气和能量载体ATP与NADPH。
- **光独立反应**：ATP和NADPH用于将二氧化碳转化为有机物，即糖类。
- **能量转换**：光能转化为化学能，最终储存在葡萄糖等有机物中。
- **碳循环**：光合作用是自然界中碳循环的重要组成部分，它固定大气中的二氧化碳，转化为有机物。

光合作用是地球上生命活动的基础，因为它不仅提供了氧气，还产生了几乎所有生命体所需的有机物质。','2025-08-28T08:58:20.149138');
INSERT INTO "ai_messages" VALUES(31,'web-yfmjk3y37br','user','好的','2025-08-28T09:03:17.787213');
INSERT INTO "ai_messages" VALUES(32,'web-yfmjk3y37br','assistant','光合作用是植物、藻类和某些细菌将光能转化为化学能的过程，主要分为光反应和暗反应。以下是光合作用的简练、条理清晰的解释：

1. **光反应**：
   - **场所**：叶绿体的类囊体膜。
   - **关键色素**：叶绿素，它吸收光能，激发电子到更高的能级。
   - **水的光解**：激发的电子用于分解水分子，生成氧气、质子和电子。
   - **ATP和NADPH的产生**：
     - **ATP的合成**：质子通过ATP合成酶梯度驱动形成ATP。
     - **NADPH的合成**：电子通过电子传递链传递给NADP+，形成NADPH。
   - **氧气释放**：水光解产生的氧气释放到大气中。

2. **暗反应**（Calvin循环）：
   - **场所**：叶绿体的基质。
   - **二氧化碳固定**：二氧化碳与一个5碳糖（RuBP）结合，生成两个3碳化合物（3-PGA）。
   - **还原反应**：利用ATP提供的能量和NADPH提供的还原力，3-PGA被还原成G3P。
   - **再生和糖类合成**：
     - 一部分G3P被转化为糖类（如葡萄糖），储存能量。
     - 其余G3P用于再生RuBP，以便循环的继续。

**关键概念与因果机制**：
- **光能的吸收**：叶绿素吸收特定波长的光能，启动光合作用。
- **光依赖性反应**：光能转化为化学能，产生氧气和能量载体ATP与NADPH。
- **光独立反应**：ATP和NADPH用于将二氧化碳转化为有机物，即糖类。
- **能量转换**：光能转化为化学能，最终储存在葡萄糖等有机物中。
- **碳循环**：光合作用固定大气中的二氧化碳，转化为有机物，是自然界中碳循环的重要组成部分。

光合作用是地球上生命活动的基础，因为它不仅提供了氧气，还产生了几乎所有生命体所需的有机物质。','2025-08-28T09:03:17.796218');
INSERT INTO "ai_messages" VALUES(37,'web-yfmjk3y37br','user','你是一位数学专家，帮我分析一下傅里叶变换的内容','2025-08-28T09:06:51.746801');
INSERT INTO "ai_messages" VALUES(38,'web-yfmjk3y37br','assistant','好的，让我们从数学的角度来分析傅里叶变换的相关内容。我会分点进行解释，并强调关键概念和因果机制。

1. **傅里叶变换的定义**：
   - **基本概念**：傅里叶变换是一种数学工具，用于将函数（或信号）从时间（或空间）域转换到频率域。它揭示了信号中不同频率成分的组成及各自的幅度和相位。
   - **因果关系**：通过傅里叶变换，可以将复杂信号分解成多个正弦波成分，其中每个正弦波对应特定的频率。这种分解有助于我们理解和分析信号的性质。

2. **傅里叶变换的类型**：
   - **连续傅里叶变换（CFT）**：适用于连续信号。将信号从时间域转换到频率域，得到频谱。
   - **离散傅里叶变换（DFT）**：适用于离散信号。是CFT的离散化版本，在数字信号处理中广泛应用。
   - **快速傅里叶变换（FFT）**：一种高效的DFT算法，大大减少了计算复杂度。通过分而治之的方法实现。

3. **傅里叶变换的性质**：
   - **线性**：傅里叶变换具有线性性质，即信号的线性组合的傅里叶变换等于各个信号变换的线性组合。
   - **时频转换**：傅里叶变换将信号的时域特性（时间信息）转换为频域特性（频率信息），反之亦然。

4. **傅里叶变换的应用**：
   - **信号处理**：分析和处理各种信号（如音频、图像、无线通信等），提取有用信息。
   - **图像分析**：通过傅里叶变换提取图像中的边缘、纹理等特征。
   - **数据压缩**：利用信号的频率特性进行压缩，如JPEG图像压缩。
   - **控制系统**：分析系统的频率响应，设计控制器。

5. **傅里叶变换的局限性**：
   - **时频分辨率**：传统傅里叶变换不能同时提供高时间分辨率和高频率分辨率，存在不确定性。
   - **非平稳信号**：对于非平稳信号（信号特性随时间变化），傅里叶变换不能提供足够的信息。

为了克服这些局限性，发展了小波变换、短时傅里叶变换等其他时频分析方法。

总之，傅里叶变换是一种强大的数学工具，通过将信号从时间域转换到频率域，揭示信号的频率成分，从而在信号处理、图像分析等领域发挥重要作用。希望以上解释能够帮助您理解傅里叶变换的关键概念和作用机制。如果还有其他问题，欢迎继续交流。','2025-08-28T09:06:51.755828');
INSERT INTO "ai_messages" VALUES(39,'web-yfmjk3y37br','user','你还是生物专家吗','2025-08-28T09:07:35.876825');
INSERT INTO "ai_messages" VALUES(40,'web-yfmjk3y37br','assistant','是的，我是生物学专家。以下是我的专业背景和能力的关键点：

1. **专业知识**：
   - 我具备丰富的生物学知识，涵盖从分子生物学到生态学等多个领域。

2. **问题解答**：
   - 我能够解答生物学相关的问题，包括概念解释、原理阐述和因果分析等。

3. **教育经验**：
   - 我能够以条理清晰的方式解释复杂概念，帮助学生理解生物学知识。

4. **信息提供**：
   - 我可以提供最新的生物学研究信息和科学发现。

5. **因果机制**：
   - 我能够解释生物学现象背后的科学原理和生物过程。

如果您有任何生物学方面的问题，无论是基础概念还是最新的研究进展，我都将竭诚为您提供准确、简练且条理清晰的回答。','2025-08-28T09:07:35.885338');
CREATE TABLE attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_id INTEGER NOT NULL,
        student_id INTEGER NOT NULL,
        status TEXT NOT NULL,
        check_in_time TIMESTAMP,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (course_id) REFERENCES courses (id),
        FOREIGN KEY (student_id) REFERENCES students (id)
    );
CREATE TABLE attendance_codes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_id INTEGER NOT NULL,
        code TEXT NOT NULL,
        expires_at TIMESTAMP NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (course_id) REFERENCES courses (id)
    );
CREATE TABLE categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        parent_id INTEGER,
        FOREIGN KEY (parent_id) REFERENCES categories (id)
    );
CREATE TABLE course_messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_id INTEGER NOT NULL,
        sender_id INTEGER NOT NULL,
        message TEXT NOT NULL,
        sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (course_id) REFERENCES courses (id),
        FOREIGN KEY (sender_id) REFERENCES users (id)
    );
CREATE TABLE course_students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_id INTEGER NOT NULL,
        student_id INTEGER NOT NULL,
        FOREIGN KEY (course_id) REFERENCES courses (id),
        FOREIGN KEY (student_id) REFERENCES students (id)
    );
CREATE TABLE courses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        teacher_id INTEGER NOT NULL,
        start_time TIMESTAMP NOT NULL,
        end_time TIMESTAMP NOT NULL,
        status TEXT NOT NULL,
        poster_url TEXT,
        video_url TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (teacher_id) REFERENCES users (id)
    );

CREATE TABLE material_tags (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        material_id INTEGER NOT NULL,
        tag_id INTEGER NOT NULL,
        FOREIGN KEY (material_id) REFERENCES materials (id),
        FOREIGN KEY (tag_id) REFERENCES tags (id)
    );
CREATE TABLE materials (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        type TEXT NOT NULL,
        url TEXT NOT NULL,
        thumbnail TEXT,
        size INTEGER NOT NULL,
        uploader_id INTEGER NOT NULL,
        category_id INTEGER,
        description TEXT,
        view_count INTEGER DEFAULT 0,
        upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (uploader_id) REFERENCES users (id),
        FOREIGN KEY (category_id) REFERENCES categories (id)
    );
CREATE TABLE messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT NOT NULL,
        sender_id INTEGER,
        recipient_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        read BOOLEAN DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (sender_id) REFERENCES users (id),
        FOREIGN KEY (recipient_id) REFERENCES users (id)
    );
CREATE TABLE paper_questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        paper_id INTEGER NOT NULL,
        question_id INTEGER NOT NULL,
        score INTEGER NOT NULL,
        FOREIGN KEY (paper_id) REFERENCES papers (id),
        FOREIGN KEY (question_id) REFERENCES questions (id)
    );
CREATE TABLE papers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        creator_id INTEGER NOT NULL,
        total_score INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (creator_id) REFERENCES users (id)
    );
CREATE TABLE questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        type TEXT NOT NULL,
        difficulty INTEGER NOT NULL,
        knowledge_point TEXT NOT NULL,
        options TEXT,
        answer TEXT NOT NULL,
        analysis TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
CREATE TABLE refresh_tokens (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                token TEXT UNIQUE NOT NULL,
                expires_at TIMESTAMP NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );
INSERT INTO "refresh_tokens" VALUES(1,2,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NTkzMTgyMSwianRpIjoiNjBiMmQ5OGQtMTU4Ny00ZjlmLTk1YzYtOGI5MjI2ZWVhOTQzIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjIsInJvbGUiOiJ0ZWFjaGVyIn0sIm5iZiI6MTc1NTkzMTgyMSwiY3NyZiI6IjAyM2E5NzlhLWY1YWMtNDJhNS04OWU1LTFhMjJiYmQzM2ZiZiIsImV4cCI6MTc1ODUyMzgyMX0.IfJPNcDf4eUSw-kTXZGzm_VUoElqT_BdqEdopaJJTRY','2025-09-22 14:50:21.078752','2025-08-23 06:50:21');
INSERT INTO "refresh_tokens" VALUES(2,2,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NTkzNjI4OSwianRpIjoiOTI4OWM2OTctNjUwMS00MzFiLWI3M2MtMDYzMDQ3ZDMzNTQwIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjIsInJvbGUiOiJ0ZWFjaGVyIn0sIm5iZiI6MTc1NTkzNjI4OSwiY3NyZiI6IjM3Y2U2NGEwLTMyOWQtNDg0Mi04YjE2LTY4ODNhMWZiMzM4NSIsImV4cCI6MTc1ODUyODI4OX0.IKUzvbVbeDJ1mm0vBi3_qxsevxdCwPnkGj41BQ-lHI4','2025-09-22 16:04:49.134388','2025-08-23 08:04:49');
INSERT INTO "refresh_tokens" VALUES(3,2,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NTkzNjYxMiwianRpIjoiZWRkOTE0OWYtZTA1Ni00NjRiLWFhMDctMDQyMmVlZmE0NjI5IiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjIsInJvbGUiOiJ0ZWFjaGVyIn0sIm5iZiI6MTc1NTkzNjYxMiwiY3NyZiI6ImE5OTU5NmY4LWIwMjctNDlkOC04MTZkLTkxMTdlNDNiZTllYSIsImV4cCI6MTc1ODUyODYxMn0.ffXu2jmsaj4c-Zhj4HlRNahXSFOYhTUGcQC95K7BaFo','2025-09-22 16:10:12.045772','2025-08-23 08:10:12');
INSERT INTO "refresh_tokens" VALUES(4,2,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NTkzOTExOSwianRpIjoiOWZhM2NlMzEtNWYxZi00MTRhLWE3YmUtMDQ5NzNlODNkMjIxIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjIsInJvbGUiOiJ0ZWFjaGVyIn0sIm5iZiI6MTc1NTkzOTExOSwiY3NyZiI6IjYzOWQ4M2JiLWViMmYtNGU4Yi05M2UyLWMwMmMwMzEzZjk4MCIsImV4cCI6MTc1ODUzMTExOX0.WVokBfBoCSJZwfSUuDOj7x4rmFE4PnRwW5ZfSEkzvxs','2025-09-22 16:51:59.772240','2025-08-23 08:51:59');
INSERT INTO "refresh_tokens" VALUES(5,2,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NTkzOTkxNywianRpIjoiMDIzYzk2NTAtZDY0MC00YTg0LWJkYzEtM2E0MmRmYjQwZmQ4IiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjIsInJvbGUiOiJ0ZWFjaGVyIn0sIm5iZiI6MTc1NTkzOTkxNywiY3NyZiI6ImYxNDcxYWNhLTZjMDktNGQ1Mi05NTE5LWRiODIyYTk1NzhiZSIsImV4cCI6MTc1ODUzMTkxN30.eH0gAKW6_DpLA-_GkBSNRngMMh-tR8i_cIg2YDut7Tk','2025-09-22 17:05:17.228472','2025-08-23 09:05:17');
INSERT INTO "refresh_tokens" VALUES(6,2,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NTk0MDA4NCwianRpIjoiOGM1OGY2ZmItZTc3Mi00ZDQxLWIwMDMtYTc0OTdmOGE5MzkxIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjIsInJvbGUiOiJ0ZWFjaGVyIn0sIm5iZiI6MTc1NTk0MDA4NCwiY3NyZiI6ImM3OWNjMDQzLWIxNjQtNDc2NS05MjRiLThjZWE5MzA5ZDVjYyIsImV4cCI6MTc1ODUzMjA4NH0.CnpCKzcS910lFU3TgcjvGQrBw44jt3JFwxgRsAswPzs','2025-09-22 17:08:04.842739','2025-08-23 09:08:04');
INSERT INTO "refresh_tokens" VALUES(7,2,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NTk0MDEyNiwianRpIjoiOTdlYjc2MjYtYjhjMC00NjNlLTljZjYtMTNlOGU1YzFlZWY1IiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjIsInJvbGUiOiJ0ZWFjaGVyIn0sIm5iZiI6MTc1NTk0MDEyNiwiY3NyZiI6ImQ1MDNjYmZkLWViYjItNGQyNC04MTRhLTVkNmY3NTNjZTA1NyIsImV4cCI6MTc1ODUzMjEyNn0.yMpEMSUvC4VhSzMLfuYTDb5Wzu3C3hgsRHLJjegN-fU','2025-09-22 17:08:46.712600','2025-08-23 09:08:46');
INSERT INTO "refresh_tokens" VALUES(8,2,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NTk0MDQxOSwianRpIjoiNmM2ODc5ODYtZjhiMi00NWVhLWE3MWUtMzc2MThhN2I0NjJiIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjIsInJvbGUiOiJ0ZWFjaGVyIn0sIm5iZiI6MTc1NTk0MDQxOSwiY3NyZiI6IjQ5NzNkZjlmLWRkOWItNDA3MC1hYjQ0LWFlZGNlNDNmMTIxNyIsImV4cCI6MTc1ODUzMjQxOX0.YO7kwcZSEk6aq99K-K6U8fMjiAnlXKCupJxeKukjdDk','2025-09-22 17:13:39.737386','2025-08-23 09:13:39');
INSERT INTO "refresh_tokens" VALUES(9,2,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NjAyNTEzNCwianRpIjoiYzc3ZDBkNDctNDU4YS00MjhkLTgzOGEtZjlmNGI4NjlkYzEwIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjIsInJvbGUiOiJ0ZWFjaGVyIn0sIm5iZiI6MTc1NjAyNTEzNCwiY3NyZiI6ImNiOTAxNGI4LThmMmMtNGJhNS1hODIyLWFiNmQ0MzIxODY3ZiIsImV4cCI6MTc1ODYxNzEzNH0.4WLm-MuQxvDtUjP2rtyfGBMYnYTrGTgaFPT2VSsvlSE','2025-09-23 16:45:34.997308','2025-08-24 08:45:34');
INSERT INTO "refresh_tokens" VALUES(10,2,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NjAyNjMyMywianRpIjoiODU4OTg5MmUtNjY5NS00MDBmLThkNzAtZTQ0ODY5NzkzMzc3IiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjIsInJvbGUiOiJ0ZWFjaGVyIn0sIm5iZiI6MTc1NjAyNjMyMywiY3NyZiI6ImQ2MDM0ZjA2LWMwNWEtNDNlOS1iYjNkLTRhOWRkYTIxM2VlMSIsImV4cCI6MTc1ODYxODMyM30.MOVXHiR1A7JAbeqf9L8WjKvP5krt71VghAAat5YhUFk','2025-09-23 17:05:23.481414','2025-08-24 09:05:23');
INSERT INTO "refresh_tokens" VALUES(11,2,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NjAyNjQ2NCwianRpIjoiZjY2YThmYTMtZWIzMS00M2NkLWJhNTEtNjBhY2JlODZkNDc5IiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjIsInJvbGUiOiJ0ZWFjaGVyIn0sIm5iZiI6MTc1NjAyNjQ2NCwiY3NyZiI6ImI2OThiOGQxLTYyMTYtNGFiNi04NTExLTMzMWVhNjY1ZmE5NCIsImV4cCI6MTc1ODYxODQ2NH0.MZVJipOhJEgFVdnlVGH1-P3qtirRayBzbWsiz4eKKJI','2025-09-23 17:07:44.184137','2025-08-24 09:07:44');
INSERT INTO "refresh_tokens" VALUES(12,2,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NjAyNzk2NCwianRpIjoiZDc2YzllY2UtMTdiZi00Yzc1LWI5ZjUtYjVmNDM3M2Q0OGY4IiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjIsInJvbGUiOiJ0ZWFjaGVyIn0sIm5iZiI6MTc1NjAyNzk2NCwiY3NyZiI6ImJmZDgwNTBjLTRlZWItNDgzMC1hZDhhLTZjYTNjMzc0NWU2YyIsImV4cCI6MTc1ODYxOTk2NH0.eu_Ek9sBVCVzMDcYdTPKQdV0-3PMjf--kFIn6NL-xDM','2025-09-23 17:32:44.327850','2025-08-24 09:32:44');
INSERT INTO "refresh_tokens" VALUES(13,2,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NjAyNzk3NCwianRpIjoiOTQ0NWU4MTctNmQ0NS00NDlkLThhYWMtMTAwYTAwYTZhZTY0IiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjIsInJvbGUiOiJ0ZWFjaGVyIn0sIm5iZiI6MTc1NjAyNzk3NCwiY3NyZiI6ImNmNWNmZDZjLTU1NTgtNGU1Ni1iOTU4LTZjZjk4ZWIyMzc5MyIsImV4cCI6MTc1ODYxOTk3NH0.kMUK5P9RwghowdxKMrrr6w4EfXXmIqanpY7QGrOH3F0','2025-09-23 17:32:54.343752','2025-08-24 09:32:54');
INSERT INTO "refresh_tokens" VALUES(14,2,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NjAyODAxMCwianRpIjoiNDI1YmQ0N2EtMmU2NS00NjBjLTg1NjEtZDQwNDMwN2ZjMzc4IiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjIsInJvbGUiOiJ0ZWFjaGVyIn0sIm5iZiI6MTc1NjAyODAxMCwiY3NyZiI6IjYwYTM1MzIzLWM3ZjUtNDViMC1iNjIwLTYwNjQ1N2VkZGY1NCIsImV4cCI6MTc1ODYyMDAxMH0.RPMVzBVQnK8RKR3RzxVKQoq3FdZh3GmLupoAgS_omKc','2025-09-23 17:33:30.960875','2025-08-24 09:33:30');
INSERT INTO "refresh_tokens" VALUES(15,2,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NjAyODEyOCwianRpIjoiYWJiNTVhZWUtZjg4NS00MzZiLTkzZDgtZTdlZDk2OWViZjFkIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjIsInJvbGUiOiJ0ZWFjaGVyIn0sIm5iZiI6MTc1NjAyODEyOCwiY3NyZiI6ImQwYmU5NzU4LWMyMDUtNGFjZS04ODlkLWExMDgzMTJiZWYzYiIsImV4cCI6MTc1ODYyMDEyOH0.25r3112LvmK5dmOs0z52GRWNFVaN0QbTdwa4IiSkH2w','2025-09-23 17:35:28.021482','2025-08-24 09:35:28');
INSERT INTO "refresh_tokens" VALUES(16,2,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NjAyODMwMiwianRpIjoiNTNiNjNlNTYtNzQ3Mi00ZmEzLWE0NWEtOWUzOTcwMDcyOWJkIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjIsInJvbGUiOiJ0ZWFjaGVyIn0sIm5iZiI6MTc1NjAyODMwMiwiY3NyZiI6ImIzNzQ1YzVkLWU1NzUtNDFiMi1hZDNmLWZiMTgxN2U0MDBlYiIsImV4cCI6MTc1ODYyMDMwMn0.v50MCmyEvfIpwDRN1n7etGR7-kQMTxm676VceDGBtu4','2025-09-23 17:38:22.426461','2025-08-24 09:38:22');
INSERT INTO "refresh_tokens" VALUES(17,2,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NjAyODMyOSwianRpIjoiMDAxZGI0YTAtNmFjNC00ZmJmLTg3MDUtNGU5MjQ5NTQyYjU2IiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjIsInJvbGUiOiJ0ZWFjaGVyIn0sIm5iZiI6MTc1NjAyODMyOSwiY3NyZiI6IjRmZmRmYzM3LTk2ZWQtNDc0MC05ZjBhLTcyZjA4OWFlZjllYiIsImV4cCI6MTc1ODYyMDMyOX0.gBKcDCKxugDpela6JfMr8lAqCpDrqAnj_C0Z9aJmZyI','2025-09-23 17:38:49.244274','2025-08-24 09:38:49');
INSERT INTO "refresh_tokens" VALUES(18,2,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NjAzMTg5NywianRpIjoiNGRlNDA4YjctMjFmNy00YTA2LWI5NWMtNDU1ODRhM2RiOGI5IiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjIsInJvbGUiOiJ0ZWFjaGVyIn0sIm5iZiI6MTc1NjAzMTg5NywiY3NyZiI6IjI5NjhiZjgxLTk2MzctNDAzZS05YzIwLTBhNmY4ZTc5NDI5MSIsImV4cCI6MTc1ODYyMzg5N30.bR6agpGtWOH7GHSXyeaMtmss1sTLIgZq0byZ3mptJ84','2025-09-23 18:38:17.677225','2025-08-24 10:38:17');
INSERT INTO "refresh_tokens" VALUES(19,2,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NjA4ODkyMiwianRpIjoiZDQyNGY4ZDktNzQ5My00ZmFhLWEyNDgtMzAyN2I4YWMzYzdkIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjIsInJvbGUiOiJ0ZWFjaGVyIn0sIm5iZiI6MTc1NjA4ODkyMiwiY3NyZiI6IjJmODBmMDFhLWNkNTktNDI3NS04MzE4LWIzMDMxMjA3ZGQ5NyIsImV4cCI6MTc1ODY4MDkyMn0.A2cnLQabj5vWXRjtrdiXXGeYKICpwj4hyjqdFn430Vk','2025-09-24 10:28:42.424446','2025-08-25 02:28:42');
INSERT INTO "refresh_tokens" VALUES(20,2,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NjA4OTQ1MSwianRpIjoiODBmYzU4YzctMzgwZi00Njk1LWEzN2QtOTg4OTc5OWExN2MyIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjIsInJvbGUiOiJ0ZWFjaGVyIn0sIm5iZiI6MTc1NjA4OTQ1MSwiY3NyZiI6Ijg4MzQ4NTA2LWU4OWItNGQ3My05NGRjLTcyODA1OGYxNGFmMiIsImV4cCI6MTc1ODY4MTQ1MX0.EvwftES4rcJObJFKIFZy5_Cl2etnZkJC2UPtFm7twzg','2025-09-24 10:37:31.977927','2025-08-25 02:37:31');
INSERT INTO "refresh_tokens" VALUES(21,2,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NjA5Mjc3NSwianRpIjoiMGIxMTY3ZjAtMzU2OC00MGFkLThmM2UtMGZhNWEzNTI5ODhjIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjIsInJvbGUiOiJ0ZWFjaGVyIn0sIm5iZiI6MTc1NjA5Mjc3NSwiY3NyZiI6IjkzZWQ2ZmUwLWI5ZWItNDVhMy1hYjI1LTZlMDkyZDhhMmM3ZiIsImV4cCI6MTc1ODY4NDc3NX0.LHruqBCpiMV7bUHkiTu69BlxianU-YGNsc_wGRPFM98','2025-09-24 11:32:55.497606','2025-08-25 03:32:55');
INSERT INTO "refresh_tokens" VALUES(22,2,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NjA5NTI4OCwianRpIjoiYWUxNWU3ZTEtMjU3NS00NTAwLWJkMGYtYWFhNWIyZTFmOWNiIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjIsInJvbGUiOiJ0ZWFjaGVyIn0sIm5iZiI6MTc1NjA5NTI4OCwiY3NyZiI6ImU3NzViZmZiLWRhNzQtNGRkZC05YTQ2LTRiNDQzZWMzY2Q5MiIsImV4cCI6MTc1ODY4NzI4OH0.9SKJI-3PB2uTDDJdJBNERtuyIyyFeBW5N0UBSvRYq6o','2025-09-24 12:14:48.777897','2025-08-25 04:14:48');
INSERT INTO "refresh_tokens" VALUES(23,2,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NjA5NjgxNCwianRpIjoiZjRhM2Q0MjMtOGViNy00MmY3LTg0NDItM2M3YTUxNzFmNDMxIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjIsInJvbGUiOiJ0ZWFjaGVyIn0sIm5iZiI6MTc1NjA5NjgxNCwiY3NyZiI6IjQ1ZDk5OTAwLTNhZmUtNGJlZS05N2RkLWJlZjk1OWI0MmE4OCIsImV4cCI6MTc1ODY4ODgxNH0.TXDRq9eNJBuEAmeoTxI84Cy_L8dpIh72dLBKasVC1TE','2025-09-24 12:40:14.986310','2025-08-25 04:40:14');
INSERT INTO "refresh_tokens" VALUES(24,2,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NjA5ODI0OSwianRpIjoiMzJhNmU0YzMtNjRiMS00MTcxLThkZjMtNWUwYWZjZGU4ZWM1IiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjIsInJvbGUiOiJ0ZWFjaGVyIn0sIm5iZiI6MTc1NjA5ODI0OSwiY3NyZiI6IjI1ZWE3MmQyLWU2NzAtNDE3Ny04YmU3LTQwMDNjNTA5MjJjMCIsImV4cCI6MTc1ODY5MDI0OX0.jiCYJ4wpMQvmX9iRmZefyGoBEmudqak_5GwFyOY_Nn8','2025-09-24 13:04:09.232564','2025-08-25 05:04:09');
INSERT INTO "refresh_tokens" VALUES(25,2,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NjA5ODYwOSwianRpIjoiZTEyYmM0ZjEtNzExNy00OTdkLWFiMjYtMDljMWY2YTliNTRhIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjIsInJvbGUiOiJ0ZWFjaGVyIn0sIm5iZiI6MTc1NjA5ODYwOSwiY3NyZiI6IjNmOWNlYmM2LWU2Y2UtNDhlMC05NzQzLTdhZDZkMjJlMWFkYiIsImV4cCI6MTc1ODY5MDYwOX0.RDNEeJC8B_rox8K_gDSEAMDDDoZIALDG-NTjTIEWleo','2025-09-24 13:10:09.779776','2025-08-25 05:10:09');
INSERT INTO "refresh_tokens" VALUES(26,2,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NjEwMzgxNywianRpIjoiNWNkMGYzMGUtNzkxMi00NmY4LThmNWQtNTA4MjA3ZGQzZjVkIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjIsInJvbGUiOiJ0ZWFjaGVyIn0sIm5iZiI6MTc1NjEwMzgxNywiY3NyZiI6IjQ3MGNlYTFkLTBiY2ItNDI1Yi1iODJiLWI2NzM2MTBmYzY2MyIsImV4cCI6MTc1ODY5NTgxN30.w2J4jZn2rSPbNbLvEcbvJnLPgV2yX4Y7a2K_EXgejSk','2025-09-24 14:36:57.399484','2025-08-25 06:36:57');
INSERT INTO "refresh_tokens" VALUES(27,2,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NjExMTgwOSwianRpIjoiNGY5YzdlYmQtY2U4Ny00ZDcwLWFmY2YtZDMxYTAxMjlmNWIzIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjIsInJvbGUiOiJ0ZWFjaGVyIn0sIm5iZiI6MTc1NjExMTgwOSwiY3NyZiI6IjUxNmYxYzQ0LWIzMmItNDNmZi1iNTVlLTZiNmE0NDk3NjRlMSIsImV4cCI6MTc1ODcwMzgwOX0.KF9ZxXhCx1ZiETUSW7OEdjys-1nEvtsflCEkn2XD_FM','2025-09-24 16:50:09.574809','2025-08-25 08:50:09');
INSERT INTO "refresh_tokens" VALUES(28,2,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NjE3ODI4NiwianRpIjoiYWI3MGYyNmUtMjViZC00MDBlLTg4OTUtOTVjOGU4OTQzODU3IiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjIsInJvbGUiOiJ0ZWFjaGVyIn0sIm5iZiI6MTc1NjE3ODI4NiwiY3NyZiI6IjgxMWNmNTI4LWY0NmQtNDg1Yy04ZjQxLWU3YzNhMjVkZjZlZCIsImV4cCI6MTc1ODc3MDI4Nn0.7-6FBJ9mOdbEqslRZQHNUgvbObD6f5zlnVMEFhNny-c','2025-09-25 11:18:06.097068','2025-08-26 03:18:06');
INSERT INTO "refresh_tokens" VALUES(29,3,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NjE5MjI0MSwianRpIjoiOWJmOWQ5MzMtYzg3MC00ZjFmLWE1ZWUtYzRhYzU0N2I4NzNjIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjMsInJvbGUiOiJzdHVkZW50In0sIm5iZiI6MTc1NjE5MjI0MSwiY3NyZiI6IjZjNWY2NDEzLTFlODMtNGQ5MS04ZjE3LTdhNjE1OThkMGRkMiIsImV4cCI6MTc1ODc4NDI0MX0.kI0GBMhgMNMrlY2Jojt6vECAJkjSnI9_I_L6UeWr5d0','2025-09-25 15:10:41.459572','2025-08-26 07:10:41');
INSERT INTO "refresh_tokens" VALUES(30,2,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NjE5MjI1MiwianRpIjoiNDk1OWRlNDktZmM4ZS00N2MxLWJkYWQtZmZjMzMzNWZmMDFhIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjIsInJvbGUiOiJ0ZWFjaGVyIn0sIm5iZiI6MTc1NjE5MjI1MiwiY3NyZiI6IjY3NjJmODc4LTBkMjYtNGM3Mi04ZjI0LTQ3NTA1MzM4OWY4ZCIsImV4cCI6MTc1ODc4NDI1Mn0.P_HH9PNYKf1ZUeiGhJJMcgvj4gNpGhflyEUr1N3bzpc','2025-09-25 15:10:52.284622','2025-08-26 07:10:52');
INSERT INTO "refresh_tokens" VALUES(31,2,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NjE5NDY3NCwianRpIjoiMjQwYmYwMmUtODQ1OS00Njk4LTk3YjYtNzlkYzMyNDIzYTRkIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjIsInJvbGUiOiJ0ZWFjaGVyIn0sIm5iZiI6MTc1NjE5NDY3NCwiY3NyZiI6ImY4NjE5MGYxLTk1YTUtNDc4OC1hMmNlLTVhNWQ3M2FmOWIwNSIsImV4cCI6MTc1ODc4NjY3NH0.K33_3uXI7PgK9NMfX8WVVLCZUuruHuPjVcXlUgi3Yo0','2025-09-25 15:51:14.588053','2025-08-26 07:51:14');
INSERT INTO "refresh_tokens" VALUES(32,2,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NjE5NzY5MiwianRpIjoiMzM2ZDk4NTgtYTlhZC00ZjdiLWIzYjAtNWE0ZjE1Yzg3OTQ4IiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjIsInJvbGUiOiJ0ZWFjaGVyIn0sIm5iZiI6MTc1NjE5NzY5MiwiY3NyZiI6ImI2MTQxYTE4LWU1ZjMtNGM2Mi1iMDlmLTc3YzRmOGY5YmY4OCIsImV4cCI6MTc1ODc4OTY5Mn0.NmsIFA1mWx-0256BRndp6K8uceOFNwJKY_Hh33N2HSI','2025-09-25 16:41:32.044983','2025-08-26 08:41:32');
INSERT INTO "refresh_tokens" VALUES(33,2,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NjE5NzkyNSwianRpIjoiOTNhODIzMGMtYTMzMi00ZDYwLWIzYzItMWY0MWFlM2FiYzQzIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjIsInJvbGUiOiJ0ZWFjaGVyIn0sIm5iZiI6MTc1NjE5NzkyNSwiY3NyZiI6ImJiNmYwMjE3LWFjYTAtNDA1NS1iMWIyLTcxYjEwNDY1NzhlZiIsImV4cCI6MTc1ODc4OTkyNX0.XWr7eNCi0iZGvjXKx-H0nbD51ACS8xegHs3h9p5kb8U','2025-09-25 16:45:25.744415','2025-08-26 08:45:25');
INSERT INTO "refresh_tokens" VALUES(34,2,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NjI2NzUxNCwianRpIjoiMGZmYTRiN2YtN2Q4OC00NGE5LWI0NmItMDM2NTViNDYzNmVlIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjIsInJvbGUiOiJ0ZWFjaGVyIn0sIm5iZiI6MTc1NjI2NzUxNCwiY3NyZiI6IjUwYzZhY2UwLThjOGItNDhhZC04ZmIxLTBlODM4NTU2ZjRmOCIsImV4cCI6MTc1ODg1OTUxNH0.mMBQXKZN7zK0ciAR_2mrDitDxEZlzNtU-SO1K1Zx9T8','2025-09-26 12:05:14.215079','2025-08-27 04:05:14');
INSERT INTO "refresh_tokens" VALUES(35,2,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NjI3MzUxOSwianRpIjoiMDA3ZmI1OTctYzI3MS00MTQ4LTgwNTktOGJjZThiNzczNzEyIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjIsInJvbGUiOiJ0ZWFjaGVyIn0sIm5iZiI6MTc1NjI3MzUxOSwiY3NyZiI6IjE1ZTg5YjQyLTE1YWYtNGRhMS04ZjRiLThiNzI4ZmM4ODM4MyIsImV4cCI6MTc1ODg2NTUxOX0.xg_hlouwzInn7514Ze3mo_gr2nW-23iIUW--SaAevI0','2025-09-26 13:45:19.641996','2025-08-27 05:45:19');
INSERT INTO "refresh_tokens" VALUES(36,2,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NjI3NTA0NSwianRpIjoiYmFjYzk5YjQtMGJhYi00NDFhLThkZTMtNGMwMDUxZjJkNWQxIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjIsInJvbGUiOiJ0ZWFjaGVyIn0sIm5iZiI6MTc1NjI3NTA0NSwiY3NyZiI6IjMzNGRkNzRmLTE2NGItNDhlYS1iOTA0LWUyNjEzZTdhZTExZSIsImV4cCI6MTc1ODg2NzA0NX0.detkhbz8JeTgSNcBHVUvjTN0a_tHwMlEa6f7cHE_8Rs','2025-09-26 14:10:45.546881','2025-08-27 06:10:45');
INSERT INTO "refresh_tokens" VALUES(37,2,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NjI3NTIxMCwianRpIjoiNzE1NzE0N2MtZWJhYS00YTljLWIzZTItMTViZDNlYWM0MDRlIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjIsInJvbGUiOiJ0ZWFjaGVyIn0sIm5iZiI6MTc1NjI3NTIxMCwiY3NyZiI6IjhjNTQwMTUxLTUzNjQtNGQ0OC04OGVlLWVkYjI5YzM4NDUyYyIsImV4cCI6MTc1ODg2NzIxMH0.LsowL8zYJT1BGfqIv7qUsejSzYfwb7Ou83Ex0e-KKqg','2025-09-26 14:13:30.599462','2025-08-27 06:13:30');
INSERT INTO "refresh_tokens" VALUES(38,2,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NjI3NjU1OSwianRpIjoiMTk1Yzg2YmQtZTJjYy00YjcyLTkyMjYtYzE3NjVmMGMxOWZiIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjIsInJvbGUiOiJ0ZWFjaGVyIn0sIm5iZiI6MTc1NjI3NjU1OSwiY3NyZiI6Ijc0ZWM5NjRjLWRmODAtNGUwNC05Y2ZlLTZhOGY2N2JjOTg2MCIsImV4cCI6MTc1ODg2ODU1OX0._9IvktSWE9LAGMgY_4QV7Jj4l3kr37eB1A1XFUGWKps','2025-09-26 14:35:59.513285','2025-08-27 06:35:59');
INSERT INTO "refresh_tokens" VALUES(39,2,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NjI3NzYyNiwianRpIjoiNDc5ODZhYjctMWYyOC00Njg4LWE0YTctZTBlMDYxYThlY2UzIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjIsInJvbGUiOiJ0ZWFjaGVyIn0sIm5iZiI6MTc1NjI3NzYyNiwiY3NyZiI6IjZmODYzMGVlLTJjMjUtNDA2Ni05Y2IxLTkyNGI1OTllZDg5YiIsImV4cCI6MTc1ODg2OTYyNn0._pST-9ebo-yyC7KZQYyoki0wVXqvWhznlv6kPYFLay0','2025-09-26 14:53:46.540687','2025-08-27 06:53:46');
INSERT INTO "refresh_tokens" VALUES(40,2,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NjI3NzgxMCwianRpIjoiMzdiOTczZDAtZWYwOC00ODQ5LTk3ZTQtYjM1NGRmMDM0MGFmIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjIsInJvbGUiOiJ0ZWFjaGVyIn0sIm5iZiI6MTc1NjI3NzgxMCwiY3NyZiI6ImVlYmM0YjJmLWRmZDgtNDY4Mi05NmIwLWYzNGE1MjBhYjZmMyIsImV4cCI6MTc1ODg2OTgxMH0.Ta6__JtLkOeNDnVb3mMhAjIZoDyQ3uBLkeIO9Pnv6KE','2025-09-26 14:56:50.354631','2025-08-27 06:56:50');
INSERT INTO "refresh_tokens" VALUES(41,3,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NjI3ODgyMSwianRpIjoiNzljNzcyYzItNGFkNy00MTMxLThiY2MtMWE0NWNjZTdjMmExIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjMsInJvbGUiOiJzdHVkZW50In0sIm5iZiI6MTc1NjI3ODgyMSwiY3NyZiI6ImU5ZjAzOGM3LWE0OWQtNDNiMi04ZDM2LTJiZjliYmVjYTg1ZCIsImV4cCI6MTc1ODg3MDgyMX0.fpYQ9I5TVsZRPufy1fXy9aZK2KUjT7DWVE2PGHvINCs','2025-09-26 15:13:41.862140','2025-08-27 07:13:41');
INSERT INTO "refresh_tokens" VALUES(42,2,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NjI3OTM5NCwianRpIjoiZjUxMTA2OTYtNjZlMC00ODk5LTk2MGItMGI1NjU0YjM4ZmM5IiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjIsInJvbGUiOiJ0ZWFjaGVyIn0sIm5iZiI6MTc1NjI3OTM5NCwiY3NyZiI6IjVjN2Q3ZmM5LTc3ZTctNGMxOS1iMjNkLTQzZDU4YjdhNmZmYiIsImV4cCI6MTc1ODg3MTM5NH0.eMZ9j4lwhsxgA58284Vvlvh4MJn0r8uKybf4PaGqTDg','2025-09-26 15:23:14.894824','2025-08-27 07:23:14');
INSERT INTO "refresh_tokens" VALUES(43,3,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NjI3OTUzNSwianRpIjoiMDUwYjI2NTktMzllOC00OWZjLWI0NTUtM2E4OWViMGFkMTVlIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjMsInJvbGUiOiJzdHVkZW50In0sIm5iZiI6MTc1NjI3OTUzNSwiY3NyZiI6IjhjMTc5YmVkLTQ3NTUtNDJkYy1iYzU1LTU3ZGVmMzliNGEwYyIsImV4cCI6MTc1ODg3MTUzNX0.1g9n3sbDRNAY9hkiJYoldgx5gqW38WKEacwFcL6IMQE','2025-09-26 15:25:35.573639','2025-08-27 07:25:35');
INSERT INTO "refresh_tokens" VALUES(44,3,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NjI3OTU0NywianRpIjoiMjQwZGIwMDMtMzBlZC00YWMwLWJiZDktYzY0ZDliNDlmNWNjIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjMsInJvbGUiOiJzdHVkZW50In0sIm5iZiI6MTc1NjI3OTU0NywiY3NyZiI6ImI4MGNmZWIzLTJlODAtNGMyNC05MDQ5LTFhODE0YzVmYmZjNyIsImV4cCI6MTc1ODg3MTU0N30.pUFfmMEswzvTXJozEfrLJA1n-7jax1LjxqP6gCKPYew','2025-09-26 15:25:47.800111','2025-08-27 07:25:47');
INSERT INTO "refresh_tokens" VALUES(45,4,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NjI3OTU3NiwianRpIjoiZmJhYzA0NDgtZmM4Ny00OWEwLWJmMmYtNWQ4NWQ4OTUyY2EyIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjQsInJvbGUiOiJzdHVkZW50In0sIm5iZiI6MTc1NjI3OTU3NiwiY3NyZiI6IjJiZTc3ZTE5LWY4MjMtNDc4MS1iYmRiLTM3NjBhM2MyMzVkZiIsImV4cCI6MTc1ODg3MTU3Nn0.im3Yol5diePtervmMTMWb4cvRhlCKPyj1lXDm4oRDis','2025-09-26 15:26:16.186407','2025-08-27 07:26:16');
INSERT INTO "refresh_tokens" VALUES(46,3,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NjI3OTc2MywianRpIjoiY2NjMzBlZTEtMmU1Mi00N2MwLWJiYzUtZmQ1NzdhMDIwNTUxIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjMsInJvbGUiOiJzdHVkZW50In0sIm5iZiI6MTc1NjI3OTc2MywiY3NyZiI6ImI3ZmM0MDQ2LTM4NzEtNGQ2OC1hMmE1LTAyNzFmYTEyMGZkNSIsImV4cCI6MTc1ODg3MTc2M30.xk-28lyy4HAN9n418vl02WDUXCMcRNenvQgpLLa3MSo','2025-09-26 15:29:23.267066','2025-08-27 07:29:23');
INSERT INTO "refresh_tokens" VALUES(47,3,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NjI4MDIwNiwianRpIjoiNDFlOTUyYTEtN2RhMS00MWY0LWFlNDgtZDY3NTlhMGVhYmJkIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjMsInJvbGUiOiJzdHVkZW50In0sIm5iZiI6MTc1NjI4MDIwNiwiY3NyZiI6Ijk3YzE2NGI4LTFhMDMtNGNmMi1iODM3LTVmMzkwNTEzMWYzNyIsImV4cCI6MTc1ODg3MjIwNn0._eqeXoIVxqtU2ghdUYS4s-2l46ugp0-euWgDyOt31Kg','2025-09-26 15:36:46.315000','2025-08-27 07:36:46');
INSERT INTO "refresh_tokens" VALUES(48,3,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NjI4MDIwNiwianRpIjoiMmZlN2U5MTctMzgyZi00Mjc1LTlkNDQtMWM4Yzg3MGRlZDIzIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjMsInJvbGUiOiJzdHVkZW50In0sIm5iZiI6MTc1NjI4MDIwNiwiY3NyZiI6ImEzY2E3MjVmLTk5YjUtNDE1My1iMDBmLTZhY2RkZjIwZTdlYiIsImV4cCI6MTc1ODg3MjIwNn0.dCRgTLnNQCIPGAqGRhXGT4BrqL40zOjBrL2-rx3gvCw','2025-09-26 15:36:46.555668','2025-08-27 07:36:46');
INSERT INTO "refresh_tokens" VALUES(49,3,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NjI4MDQ1OCwianRpIjoiOGFjM2M2ZjYtMTNkZi00YjhmLWJkZDktYzlkOWVkMDkxYzIxIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjMsInJvbGUiOiJzdHVkZW50In0sIm5iZiI6MTc1NjI4MDQ1OCwiY3NyZiI6Ijc3YWY4YmI3LWNhM2MtNDY5NS1hNmQ2LThjNjc4MTFiMzQzZSIsImV4cCI6MTc1ODg3MjQ1OH0.aZvF3aGVicKi-Zl5NTaSRjvHWvWd0equi5IKEpN6XRo','2025-09-26 15:40:58.396103','2025-08-27 07:40:58');
INSERT INTO "refresh_tokens" VALUES(50,3,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NjI4MDQ1OCwianRpIjoiZTVlZWVmM2YtN2ZkZC00YjljLTgxMTgtMDNlMzNiNWIwMDIyIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjMsInJvbGUiOiJzdHVkZW50In0sIm5iZiI6MTc1NjI4MDQ1OCwiY3NyZiI6IjU4OTJjMGU0LTU5NjUtNGJhNS04OTE0LTFiYzA3OTdkMTdiZiIsImV4cCI6MTc1ODg3MjQ1OH0.P4HhfQO5q0lz-c6n_TEfatIBZ6qMgd86an6ImQ5v-w4','2025-09-26 15:40:58.648541','2025-08-27 07:40:58');
INSERT INTO "refresh_tokens" VALUES(51,3,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NjI4MDQ3NiwianRpIjoiZThmNzY1M2ItMTNlZC00MzYwLTkwY2QtZDQ1ZWYyOWZlM2YxIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjMsInJvbGUiOiJzdHVkZW50In0sIm5iZiI6MTc1NjI4MDQ3NiwiY3NyZiI6ImZkMDYyNjJlLTM0YTEtNDA5NC04NTVjLWFiYjE3ODQ2MTYzMCIsImV4cCI6MTc1ODg3MjQ3Nn0.rcrxq5rc1uRkhfqG_8ghgCijcNbptKZB_7p2L4I5nJE','2025-09-26 15:41:16.562714','2025-08-27 07:41:16');
INSERT INTO "refresh_tokens" VALUES(52,3,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NjI4MDQ3NiwianRpIjoiZDRiODM2ODMtNTM1Yi00ZWUzLWFkZDItOGE5MjY2N2Y3M2U3IiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjMsInJvbGUiOiJzdHVkZW50In0sIm5iZiI6MTc1NjI4MDQ3NiwiY3NyZiI6ImE0MzhmZGVlLTRiYjgtNDUzOS05OWJiLTZiY2IzMjA2OWNlYiIsImV4cCI6MTc1ODg3MjQ3Nn0.YSHEdZeINcHb2awZGFD9twkQecdvMt7-o8Nd8E-flqc','2025-09-26 15:41:16.879334','2025-08-27 07:41:16');
INSERT INTO "refresh_tokens" VALUES(53,3,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NjI4MDU3MSwianRpIjoiZmQ4M2IzNWQtYThhMS00ZTk3LTgwOTAtODMxNTdiMmQwYjQwIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjMsInJvbGUiOiJzdHVkZW50In0sIm5iZiI6MTc1NjI4MDU3MSwiY3NyZiI6IjA2NzQyMzhiLTkzMTQtNDA1Ny1iZmEwLWQ0MTM4MWZmN2EzYSIsImV4cCI6MTc1ODg3MjU3MX0.ehd0FIVkrYMma6qSt2PT7nQydxjjyHRjrMIwJudsIVE','2025-09-26 15:42:51.944099','2025-08-27 07:42:51');
INSERT INTO "refresh_tokens" VALUES(54,3,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NjI4MDU3MiwianRpIjoiODU0ZjE5ZGItNTY1ZC00MGM5LThkNjEtYjY4YTI2MTY5OGY4IiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjMsInJvbGUiOiJzdHVkZW50In0sIm5iZiI6MTc1NjI4MDU3MiwiY3NyZiI6IjZlZDljNWMwLTQ3ZjYtNGI2ZS1hYjFmLTAxOWViZDIxZTYyMyIsImV4cCI6MTc1ODg3MjU3Mn0.oL8-V2trX_VYUKAo9z4hv5q44sGgMlyOEBDGEdvrgcI','2025-09-26 15:42:52.188026','2025-08-27 07:42:52');
INSERT INTO "refresh_tokens" VALUES(55,3,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NjI4MDgzNiwianRpIjoiOTlkMzEwZDgtMjU3Ni00ZTI2LWIwOWUtODhkNzZiNDQxOGY3IiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjMsInJvbGUiOiJzdHVkZW50In0sIm5iZiI6MTc1NjI4MDgzNiwiY3NyZiI6ImEwNzVlMDg3LTg3OGYtNDYyZS05YTM3LWEwYzAzMjQzMjRiYyIsImV4cCI6MTc1ODg3MjgzNn0.BlAG_coSpwabUNoYFcJZSyaKRn7sipDTWguCl7GKWIw','2025-09-26 15:47:16.499056','2025-08-27 07:47:16');
INSERT INTO "refresh_tokens" VALUES(56,3,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NjI4MDgzNiwianRpIjoiZjljNGQ3ZWMtOWVkNi00NDI4LTkzYWMtMzNhYmI3MWVmNTdhIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjMsInJvbGUiOiJzdHVkZW50In0sIm5iZiI6MTc1NjI4MDgzNiwiY3NyZiI6ImJlMWI2OWRlLTJlN2YtNDAxNi04MWUxLWMyNGQ1ZTc3NzY4YiIsImV4cCI6MTc1ODg3MjgzNn0.xcW6KYZMsqNAzcWqph8uLc1R5TPeFJiVKttpGUqSfJY','2025-09-26 15:47:16.764293','2025-08-27 07:47:16');
INSERT INTO "refresh_tokens" VALUES(57,3,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NjI4MTM5MSwianRpIjoiNjE3ODk1ODgtMmJhMi00YTY5LWJjZWItNTFjNGI5MjUyMDJjIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjMsInJvbGUiOiJzdHVkZW50In0sIm5iZiI6MTc1NjI4MTM5MSwiY3NyZiI6IjA2ZWRiNWZhLTMzNzItNDUxNi1iZmE5LTA1ZDgyMTYxOWFmOCIsImV4cCI6MTc1ODg3MzM5MX0.Ds6hKfIWYZduibGuSPOUc4dezPes-aHuIK5PVrl32gM','2025-09-26 15:56:31.749558','2025-08-27 07:56:31');
INSERT INTO "refresh_tokens" VALUES(58,3,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NjI4MTM5MSwianRpIjoiNWNmZmNjYmItMGM1ZS00YWZlLTgwMjktMmJkNTlmMWVlNTVlIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjMsInJvbGUiOiJzdHVkZW50In0sIm5iZiI6MTc1NjI4MTM5MSwiY3NyZiI6ImVlZDgyNTczLWU3YzEtNDc4MC1hNDExLWI4YmU3MzUyNzgyNSIsImV4cCI6MTc1ODg3MzM5MX0.kb0c_7vOr6LaP8jRvE2nIxB_ASztuELXYO2uSHJYOw4','2025-09-26 15:56:31.931341','2025-08-27 07:56:31');
INSERT INTO "refresh_tokens" VALUES(59,3,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NjI4MTM5MSwianRpIjoiM2RhNTdkNDMtNzk5Yi00Yzk4LTg0MzItOGE5YzkyOWVmODVjIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjMsInJvbGUiOiJzdHVkZW50In0sIm5iZiI6MTc1NjI4MTM5MSwiY3NyZiI6ImVkYjNkMGMxLWYwNDItNDY1ZS04ZmJiLWQ2NjMwNjc3YmQ1YiIsImV4cCI6MTc1ODg3MzM5MX0.1eDVGhcugFyEMM4-A8cYQk-qcnPoMDLhVM1UWxAuVbQ','2025-09-26 15:56:31.970383','2025-08-27 07:56:31');
INSERT INTO "refresh_tokens" VALUES(60,2,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NjI4MTQxNCwianRpIjoiZDUzYmY3NGUtYTQ1Mi00MTNhLTllZmItZmFlNGU0ZjlhNzU3IiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjIsInJvbGUiOiJ0ZWFjaGVyIn0sIm5iZiI6MTc1NjI4MTQxNCwiY3NyZiI6IjIzYWJkMzI0LWI4MDktNDc2MS05NzQ0LTY3YzBmZjA1MjliNCIsImV4cCI6MTc1ODg3MzQxNH0.5mD1ZxDBjsZ-z_sgJSXIy6tpaekhy9uh2Osyqia3R94','2025-09-26 15:56:54.481856','2025-08-27 07:56:54');
INSERT INTO "refresh_tokens" VALUES(61,2,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NjI4MTQxNCwianRpIjoiMmIxY2JjNmEtMjQ0Ny00MDg4LTg2MDMtODQ1ZmU5OTc4OTdmIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjIsInJvbGUiOiJ0ZWFjaGVyIn0sIm5iZiI6MTc1NjI4MTQxNCwiY3NyZiI6IjczODAzMzQ1LWE3M2YtNDc4Yy1hNTQxLTk0MzEwNTYzMWVhMSIsImV4cCI6MTc1ODg3MzQxNH0.LCaKN5qvVeMqjyvJNbInPm-KXm7nZqJ3DIKSqQRrtTs','2025-09-26 15:56:54.564959','2025-08-27 07:56:54');
INSERT INTO "refresh_tokens" VALUES(62,2,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NjI4MTQxNCwianRpIjoiODQ5NTVjNDUtN2QxMS00OGU1LThhYWMtNmEzZmNhOTc3MDc3IiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjIsInJvbGUiOiJ0ZWFjaGVyIn0sIm5iZiI6MTc1NjI4MTQxNCwiY3NyZiI6IjBkZDE4NGFkLTgyNjMtNDI4Yi1iZWQwLWVjNjFhZDM3ODUzNyIsImV4cCI6MTc1ODg3MzQxNH0.-qc-H3D4UWIrheZiXcxMOfxMSv5L4ADNncWZVnrOXPQ','2025-09-26 15:56:54.811955','2025-08-27 07:56:54');
INSERT INTO "refresh_tokens" VALUES(63,3,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NjI4MjA0NywianRpIjoiNTk5ZjRkYTgtNWEzMy00NjY4LWE5Y2EtODhmM2EzYzM1ZTZkIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjMsInJvbGUiOiJzdHVkZW50In0sIm5iZiI6MTc1NjI4MjA0NywiY3NyZiI6IjFlZjMyYzRmLTAxMTEtNGUwMy1hNGJlLWQ1OTFjYTY1OTkxNSIsImV4cCI6MTc1ODg3NDA0N30.ZKPfq8DRdNW94Pf6wjEK-gjff5LU98irNomMZ4CydRg','2025-09-26 16:07:27.206241','2025-08-27 08:07:27');
INSERT INTO "refresh_tokens" VALUES(64,3,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NjI4MjEzMCwianRpIjoiNGRlYTZjMzAtYWQ0NS00MDQzLTg5MmQtMGY2N2Q4MzVhZTc5IiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjMsInJvbGUiOiJzdHVkZW50In0sIm5iZiI6MTc1NjI4MjEzMCwiY3NyZiI6ImM0ZWQyNWYwLWUxYzktNGFkYS1hZWYzLTdmNjA4ZGQ3YTkyMiIsImV4cCI6MTc1ODg3NDEzMH0.02luMliBQiFLhwD-q_w0QurRMyDgU24LucK62pwIu3M','2025-09-26 16:08:50.419300','2025-08-27 08:08:50');
INSERT INTO "refresh_tokens" VALUES(65,3,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NjI4MjQ4NSwianRpIjoiMDM0MjM3MWEtMTZkNS00ZmU2LTlmZDUtN2NkMDYxMWRhYzExIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjMsInJvbGUiOiJzdHVkZW50In0sIm5iZiI6MTc1NjI4MjQ4NSwiY3NyZiI6ImUwYmEyZmZmLTFhMjgtNDg1OC1hOTE5LTI1MzI3N2NjZTk1NCIsImV4cCI6MTc1ODg3NDQ4NX0.6vT8w_sw4LGNNd5n4rayQOxd8Qwue0rur6ZzziErgbg','2025-09-26 16:14:45.429197','2025-08-27 08:14:45');
INSERT INTO "refresh_tokens" VALUES(66,3,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NjI4MjYzNSwianRpIjoiN2FmYzRjMzItOWY2MC00OTA0LWJiMjktOGFiOTg2OGVjNGI1IiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjMsInJvbGUiOiJzdHVkZW50In0sIm5iZiI6MTc1NjI4MjYzNSwiY3NyZiI6IjgyZTVlMjY2LTQzMGUtNGIwMi04N2MzLTMzZTFlYjhkODM2MSIsImV4cCI6MTc1ODg3NDYzNX0.TcWBvX-CQzN02MRG_O-l_Ld1eU1JBg91gcRf_TbnrrM','2025-09-26 16:17:15.656727','2025-08-27 08:17:15');
INSERT INTO "refresh_tokens" VALUES(67,3,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NjI4MjcxMSwianRpIjoiMzY4ZWJiZmEtYjZmOC00Y2U5LWIzZWMtNDA5NWFjN2EwN2MwIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjMsInJvbGUiOiJzdHVkZW50In0sIm5iZiI6MTc1NjI4MjcxMSwiY3NyZiI6IjA0MWRmODEyLTg3NzQtNDJlNy04ZTJjLWRiYmI4YjhlMWIxOCIsImV4cCI6MTc1ODg3NDcxMX0.fBgXUkROSvFi_HWR4r0929wNSObQWYfbEklMFsHfhZ4','2025-09-26 16:18:31.216934','2025-08-27 08:18:31');
INSERT INTO "refresh_tokens" VALUES(68,3,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NjI4Mjg4MiwianRpIjoiMjJlZDFiMTAtYzBhOC00MGM1LTk2ZjEtMjljNTNjODk4MDdhIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjMsInJvbGUiOiJzdHVkZW50In0sIm5iZiI6MTc1NjI4Mjg4MiwiY3NyZiI6ImRlNDRlY2JjLTE4YjAtNGM0OS1hY2Y5LThmMGMwODdmMDExNCIsImV4cCI6MTc1ODg3NDg4Mn0.ufqAUosr6kjA8BwVCPeWT01Ub4e64_GvHeEQcg5ObrE','2025-09-26 16:21:22.289008','2025-08-27 08:21:22');
INSERT INTO "refresh_tokens" VALUES(69,3,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NjI4MzAxNCwianRpIjoiNDdiYzlhZmUtMTM4OC00M2EzLTk4ODUtYTFlNTlmZWQxZDc1IiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjMsInJvbGUiOiJzdHVkZW50In0sIm5iZiI6MTc1NjI4MzAxNCwiY3NyZiI6ImViYmYxMzgyLWM1ZmItNGQ4NC04NjhiLWJiY2IyZGEwMWRkNiIsImV4cCI6MTc1ODg3NTAxNH0.5ABrrFv0vgLt9XhfuXIdjWIIknCtoub3TFajXuSmSKw','2025-09-26 16:23:34.816288','2025-08-27 08:23:34');
INSERT INTO "refresh_tokens" VALUES(70,3,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NjI4MzE1NCwianRpIjoiMGUzZTRjOTQtMjJkZi00ZWUyLThiZGUtNDFjNWNmMDA5ZTZmIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjMsInJvbGUiOiJzdHVkZW50In0sIm5iZiI6MTc1NjI4MzE1NCwiY3NyZiI6IjcxNTJiNGYxLThmNjUtNDUzZi04MWNlLTVmZWRiMzFiZTA0OCIsImV4cCI6MTc1ODg3NTE1NH0.mz4YjJQBHaE2nvBJQmx503wr2MoJhRxMafIXczaDOMk','2025-09-26 16:25:54.694325','2025-08-27 08:25:54');
INSERT INTO "refresh_tokens" VALUES(71,3,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NjI4MzIwNSwianRpIjoiM2UxM2UxMDMtOTc2NS00MTYzLTg2ZTQtMDZjZDAwYjVhMDU4IiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjMsInJvbGUiOiJzdHVkZW50In0sIm5iZiI6MTc1NjI4MzIwNSwiY3NyZiI6IjNlOGMyOTg3LTZjYTUtNDBkYS1hM2Q5LWJkMjU5OWQwNmJjMCIsImV4cCI6MTc1ODg3NTIwNX0.yzGb6kEVepXz8cvPZpQZh5fI702JOF3UX3CZy1SkbZo','2025-09-26 16:26:45.174835','2025-08-27 08:26:45');
INSERT INTO "refresh_tokens" VALUES(72,3,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NjI4MzM2MSwianRpIjoiY2MwN2ExZDYtMzFjNy00NWQ4LThmMWQtYTI5ZjgxZGMzMmQyIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjMsInJvbGUiOiJzdHVkZW50In0sIm5iZiI6MTc1NjI4MzM2MSwiY3NyZiI6ImUyMzUyZmZkLWI2MjgtNGZiYy1hOTRhLWQwOGM4NGVlMDI5MCIsImV4cCI6MTc1ODg3NTM2MX0.P8LkvBipQizNwkwlr5sVUc_rABRYgXvovqRohbGzxJ4','2025-09-26 16:29:21.281033','2025-08-27 08:29:21');
INSERT INTO "refresh_tokens" VALUES(73,3,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NjI4MzQ2MSwianRpIjoiYmFjNTM1YjgtNDczMC00NDZiLThmOGYtYzA1ZWIzZWY4ZmM1IiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjMsInJvbGUiOiJzdHVkZW50In0sIm5iZiI6MTc1NjI4MzQ2MSwiY3NyZiI6IjFlOWU1YTMzLWJiNjQtNGIwNC1hMTMzLTExNzJiZTE1ZGZlNyIsImV4cCI6MTc1ODg3NTQ2MX0.PTZr4clA0HtVJ7LtbpJysHuNmM2qGNx9kv4184hVbZk','2025-09-26 16:31:01.438088','2025-08-27 08:31:01');
INSERT INTO "refresh_tokens" VALUES(74,3,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NjI4OTMyMiwianRpIjoiNzAwODZhYmQtOWM1MC00Mzc1LWEwNTctOTE3MGM5NjhkNTE0IiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjMsInJvbGUiOiJzdHVkZW50In0sIm5iZiI6MTc1NjI4OTMyMiwiY3NyZiI6IjUzNzgzOWIwLWIxMjQtNDhlZC1hN2IxLThjZjI1ZDRlNGVmMCIsImV4cCI6MTc1ODg4MTMyMn0.ES5IIYdwpZSc6w881xLO1VXJrV4jJvPRcQQn5hu7x7o','2025-09-26 18:08:42.074759','2025-08-27 10:08:42');
INSERT INTO "refresh_tokens" VALUES(75,3,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NjI4OTM5NiwianRpIjoiN2VhM2MwN2MtMDFkNS00MGU3LTkwNjQtMDNmMTJlODViMjU5IiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjMsInJvbGUiOiJzdHVkZW50In0sIm5iZiI6MTc1NjI4OTM5NiwiY3NyZiI6ImMxYTZiNDk0LTQzNzAtNGQzYy1hMTkzLWQ0ZjRlMzg5YjNjYyIsImV4cCI6MTc1ODg4MTM5Nn0.4XvbODww2rO-P1iIhHFw8ZKyX7XQqj9xwUfUPkRU_a4','2025-09-26 18:09:56.611761','2025-08-27 10:09:56');
INSERT INTO "refresh_tokens" VALUES(76,3,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NjI4OTUwMCwianRpIjoiYThhMWM0NTYtMmI5OS00N2UwLWFhNWMtYjMxMzhkOTJjMTgxIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjMsInJvbGUiOiJzdHVkZW50In0sIm5iZiI6MTc1NjI4OTUwMCwiY3NyZiI6Ijk3MDE1MmEwLTMwMTUtNDU2ZC05NGI3LWE4NjIzNmVjMzNjNSIsImV4cCI6MTc1ODg4MTUwMH0.0ea-8oUqpVPTXjxa_B9wcLa1RwYK8D6xjY8nrHEIT7o','2025-09-26 18:11:40.303905','2025-08-27 10:11:40');
INSERT INTO "refresh_tokens" VALUES(77,3,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NjI4OTYyMSwianRpIjoiNjY5Y2EyODUtZGVhMy00ODg1LThkMzUtOTU0NDUyOGE5NmNlIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjMsInJvbGUiOiJzdHVkZW50In0sIm5iZiI6MTc1NjI4OTYyMSwiY3NyZiI6IjkzZWVjOTQ0LTA2YTAtNDM0MS1hYTc3LTA5NGQ4MzFjNmIyMiIsImV4cCI6MTc1ODg4MTYyMX0.4bwjwuoj551N86sBZGQFTcUV2heNJXoGG3on9ex4F6E','2025-09-26 18:13:41.084928','2025-08-27 10:13:41');
INSERT INTO "refresh_tokens" VALUES(78,3,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NjI4OTgwNiwianRpIjoiYTE2MDBiZmUtNWRhZS00ZWU5LTkyNzUtNDk0ZjYwMGQ0MTc4IiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjMsInJvbGUiOiJzdHVkZW50In0sIm5iZiI6MTc1NjI4OTgwNiwiY3NyZiI6ImE4NTdhNTI1LTllNmMtNDlhYi1iNGZiLWQ4YmQ5NGE0OGUyZSIsImV4cCI6MTc1ODg4MTgwNn0.ZP9Oy9L-Oeffb4yo2jkrmlcDEdUFIAlU0h3t2KWbxWM','2025-09-26 18:16:46.884809','2025-08-27 10:16:46');
INSERT INTO "refresh_tokens" VALUES(79,3,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NjI5MTAxOSwianRpIjoiNjMwM2M3OGQtMTVhZi00ZjI0LTllNjAtNGJiOGJlZGY1Yzg3IiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjMsInJvbGUiOiJzdHVkZW50In0sIm5iZiI6MTc1NjI5MTAxOSwiY3NyZiI6IjM1YTI2MTA2LWVmYjctNGQ4OS1iOWQ5LTY4OGE2ZDcyYzJmNyIsImV4cCI6MTc1ODg4MzAxOX0.b2rMNBAU3Gy78rxnhLGSSvUjWf5--r-ZRyialrIPtXk','2025-09-26 18:36:59.661233','2025-08-27 10:36:59');
INSERT INTO "refresh_tokens" VALUES(80,3,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NjI5MTE3NywianRpIjoiOTExMmViMzItYTE3NC00YmUzLWE3YTAtMzQ3MDYzMzg1YTc5IiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjMsInJvbGUiOiJzdHVkZW50In0sIm5iZiI6MTc1NjI5MTE3NywiY3NyZiI6ImYwMGIzOTdiLWQ2NzctNGY1YS1iZGM2LWU1M2Y1ZmE2NmM1NyIsImV4cCI6MTc1ODg4MzE3N30.JfLHNDWLsxhBe9jRTCEyaSwEWAZcxS356PdFBUXao7A','2025-09-26 18:39:37.015287','2025-08-27 10:39:37');
INSERT INTO "refresh_tokens" VALUES(81,3,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NjI5MTQ0NCwianRpIjoiM2ZjOTQ0NTUtZDNmOS00NTU1LTg5MzItYTkxYWRjOTJjY2Q0IiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjMsInJvbGUiOiJzdHVkZW50In0sIm5iZiI6MTc1NjI5MTQ0NCwiY3NyZiI6IjJkMDhiNWQ5LTE1MmMtNDdjNy1hYTI0LTRlYTg5NTZjZGVlNSIsImV4cCI6MTc1ODg4MzQ0NH0.sRmAPr9eheSOJRfuZcMRsQNuEKaoKUrjIHr9gGceds0','2025-09-26 18:44:04.045085','2025-08-27 10:44:04');
INSERT INTO "refresh_tokens" VALUES(82,3,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NjI5MzEwNywianRpIjoiZGU3MzhmYzgtMmUzYS00YWUyLWEwYzctNTI0YmY2Njk5MDcwIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjMsInJvbGUiOiJzdHVkZW50In0sIm5iZiI6MTc1NjI5MzEwNywiY3NyZiI6IjU5MGQ4YWY3LWZmYmQtNGJiNC1hNDQ2LTAwYzVkOGU2ZmQyZiIsImV4cCI6MTc1ODg4NTEwN30.4Ng-8BrL3oSQlMyxz8_9IwzH1oW8tvDBvg_O_1e4P5I','2025-09-26 19:11:47.622281','2025-08-27 11:11:47');
INSERT INTO "refresh_tokens" VALUES(83,2,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NjI5NTE3NiwianRpIjoiMzRjMjg3MDktOTJlMS00NDBlLTllMTEtNzkxN2ViYmI2NzZlIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjIsInJvbGUiOiJ0ZWFjaGVyIn0sIm5iZiI6MTc1NjI5NTE3NiwiY3NyZiI6IjU2MzMzMDIwLWU4N2ItNGE4Mi04MGZhLTkxYTNkMTVlNmYwNyIsImV4cCI6MTc1ODg4NzE3Nn0.YRJ0Fg73r1fswxYpOTNK4OrRMdocbazVS1MVGZZl9EI','2025-09-26 19:46:16.095554','2025-08-27 11:46:16');
INSERT INTO "refresh_tokens" VALUES(84,3,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NjI5NTc1NiwianRpIjoiMjM2Mjc0NDgtN2Q1My00ZWVkLTk2MjctZTFjYjJjYjgzM2ZmIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjMsInJvbGUiOiJzdHVkZW50In0sIm5iZiI6MTc1NjI5NTc1NiwiY3NyZiI6ImYzZWRhMWNkLTdkZmUtNGZmMy05YzFiLTUxOWVhMzA5YzUxMSIsImV4cCI6MTc1ODg4Nzc1Nn0.Vr14tKMtc1fAyw3eM39t6DeRoVk28VRJFwSqGjkA-y8','2025-09-26 19:55:56.957249','2025-08-27 11:55:56');
INSERT INTO "refresh_tokens" VALUES(85,3,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NjI5NTk5MywianRpIjoiZTg4ZjE4NGQtYmYwMS00ZmEyLTlmZTgtMTI4NjM1MjY4OTQ3IiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjMsInJvbGUiOiJzdHVkZW50In0sIm5iZiI6MTc1NjI5NTk5MywiY3NyZiI6IjE4MzM0ZWVhLTkyMTYtNDExYS04OTQyLWY4ODU3NTg1YzA5NiIsImV4cCI6MTc1ODg4Nzk5M30.82Njt9nX4qHRNq0_hZKvVtNeJK94YhUxwey3g8_dpo4','2025-09-26 19:59:53.633397','2025-08-27 11:59:53');
INSERT INTO "refresh_tokens" VALUES(86,3,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NjM0OTAzOCwianRpIjoiYjIyOWQyOTItNTBmNy00ZDBjLTgwZWQtM2Y1ZjIyYzJkN2RjIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjMsInJvbGUiOiJzdHVkZW50In0sIm5iZiI6MTc1NjM0OTAzOCwiY3NyZiI6ImVkNmI5NGVhLWE5MjQtNDA1Ny05M2Q2LTczODVmMTUzNThlZCIsImV4cCI6MTc1ODk0MTAzOH0.4BnXyCgqLvxKS1D2WiLvvOxl1bYtgL2UskiZOqGa2TU','2025-09-27 10:43:58.157108','2025-08-28 02:43:58');
INSERT INTO "refresh_tokens" VALUES(87,2,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NjM0OTQwNywianRpIjoiOWNmNGYyZGQtOWMwMi00NzM0LWI3MzgtNDQwOWIwNGQxMjczIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjIsInJvbGUiOiJ0ZWFjaGVyIn0sIm5iZiI6MTc1NjM0OTQwNywiY3NyZiI6Ijk5ZGI4ZjNiLTQ2ZTAtNGZlZi1iMGViLTY5YmY3ZWQ2MWM2YyIsImV4cCI6MTc1ODk0MTQwN30.t2bGmH402LKMIdUAO-0eizfTryhoDqIFm6F3ttRmjZo','2025-09-27 10:50:07.244239','2025-08-28 02:50:07');
INSERT INTO "refresh_tokens" VALUES(88,3,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NjM0OTU4MSwianRpIjoiNTQ2ZTViZGMtNTBmNi00MzRjLWI1OTMtMzA5YTIxNDFkODUyIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjMsInJvbGUiOiJzdHVkZW50In0sIm5iZiI6MTc1NjM0OTU4MSwiY3NyZiI6IjE3ZjU3ODY2LTc5NTUtNGE4MC04MmNlLTIxMGU4YWRjNzcxMSIsImV4cCI6MTc1ODk0MTU4MX0.KyT8W6nE6RL8i9Kf7_221x1F8545G4k4mXNjTLmCWQQ','2025-09-27 10:53:01.311468','2025-08-28 02:53:01');
INSERT INTO "refresh_tokens" VALUES(89,2,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NjM0OTU5OSwianRpIjoiNTYyMDkzMTEtYWQ5NS00NzNiLTljMmEtZDM2NmU5MmNkOGMxIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjIsInJvbGUiOiJ0ZWFjaGVyIn0sIm5iZiI6MTc1NjM0OTU5OSwiY3NyZiI6Ijk3ZGFhNTUzLWQ5MmQtNDQzZi04YjhkLTg5ODM4OTM1ZmZiMiIsImV4cCI6MTc1ODk0MTU5OX0.9px67q3eWa7x5nubonpTxR9myXNhy5jAUlaXsaw23B8','2025-09-27 10:53:19.280445','2025-08-28 02:53:19');
INSERT INTO "refresh_tokens" VALUES(90,3,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NjM1MTE1NCwianRpIjoiNjJiZGI1YjgtOTEzZS00MWI2LTg1MjItZmIxYjhiNDEwMTcxIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjMsInJvbGUiOiJzdHVkZW50In0sIm5iZiI6MTc1NjM1MTE1NCwiY3NyZiI6IjZkNmJiYTFkLTUwZDYtNDhkOS05NjRlLTgwNzU2N2I1NzA2YyIsImV4cCI6MTc1ODk0MzE1NH0.mZlHF3I-h_dx6YUVs21_QHsH2_cng4yPgGqlH_uIcyI','2025-09-27 11:19:14.886413','2025-08-28 03:19:14');
INSERT INTO "refresh_tokens" VALUES(91,3,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NjM2MDIxNSwianRpIjoiYzRiMjY1YTctNjM3Ni00M2I5LWI5MWEtYzEwNWQ0OGM4MjBmIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjMsInJvbGUiOiJzdHVkZW50In0sIm5iZiI6MTc1NjM2MDIxNSwiY3NyZiI6IjAxZjU1OWE2LTljN2UtNDMwZS05YTEwLTNjMmYyYTc3NjdhMSIsImV4cCI6MTc1ODk1MjIxNX0.-DHcTKhdBGNbRZXYwnH4GuItJKyFYry69dUcmbJwsY0','2025-09-27 13:50:15.775736','2025-08-28 05:50:15');
INSERT INTO "refresh_tokens" VALUES(92,3,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NjM2NzUzNywianRpIjoiOTQ5MmMxMTItYWFjOC00NmEyLThlM2YtZmEzMWYwY2ZjOTgzIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjMsInJvbGUiOiJzdHVkZW50In0sIm5iZiI6MTc1NjM2NzUzNywiY3NyZiI6IjY5MTgzMDViLTYxYjktNGIxZS1hNDliLWI4YmY1NzYxNDE4NiIsImV4cCI6MTc1ODk1OTUzN30.LBJ3_IY7OqCZkj-DIT3Ro3gUGjY3PbpWZBI_MCQOa8Y','2025-09-27 15:52:17.547081','2025-08-28 07:52:17');
INSERT INTO "refresh_tokens" VALUES(93,3,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NjM2OTg4MSwianRpIjoiMDllNjJlNjQtNDE0NC00ZGFlLWE1NGUtMzViMTc5OGJhMzFiIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjMsInJvbGUiOiJzdHVkZW50In0sIm5iZiI6MTc1NjM2OTg4MSwiY3NyZiI6ImRiY2IyMWFlLTE2MzctNDJlZC1iMGJkLWJiMWY5ZmEwNzE0NiIsImV4cCI6MTc1ODk2MTg4MX0.rXqgpFzi6e02Dby1niIsgLJ9LwTMFix2ad7MbG4N79g','2025-09-27 16:31:21.307729','2025-08-28 08:31:21');
INSERT INTO "refresh_tokens" VALUES(94,3,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NjM3MDMzMCwianRpIjoiMDZmNTVmNGQtYmYwOC00N2E1LWFmZTQtZDFlZTBkNzZlOTc1IiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjMsInJvbGUiOiJzdHVkZW50In0sIm5iZiI6MTc1NjM3MDMzMCwiY3NyZiI6IjIwMGU5YTJlLWExMmUtNDZkOC1hNTk3LTg1MjViZmMzODI3MCIsImV4cCI6MTc1ODk2MjMzMH0.XsuxhlyrycLJEEeC8bFkcg3_ZuBUSrZ7HX6rckGAxv0','2025-09-27 16:38:50.107641','2025-08-28 08:38:50');
INSERT INTO "refresh_tokens" VALUES(95,3,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NjM3MTQ2MiwianRpIjoiNjFjODJkMzMtMTkxNi00Mzc4LWJhMTUtYzMxN2FjNjVjODc4IiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjMsInJvbGUiOiJzdHVkZW50In0sIm5iZiI6MTc1NjM3MTQ2MiwiY3NyZiI6IjQxM2E0NDBlLTVhOWYtNDNmMC1iNWIyLTQ2NGU1YWYzOTM1OCIsImV4cCI6MTc1ODk2MzQ2Mn0.5FzAexajXg1GVO8xYxMrvcDVdV9yc_mnbqFBeqIVBPs','2025-09-27 16:57:42.439155','2025-08-28 08:57:42');
DELETE FROM "sqlite_sequence";
INSERT INTO "sqlite_sequence" VALUES('users',71);
INSERT INTO "sqlite_sequence" VALUES('refresh_tokens',95);
INSERT INTO "sqlite_sequence" VALUES('ai_messages',40);
CREATE TABLE students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        student_id TEXT UNIQUE NOT NULL,
        class TEXT NOT NULL,
        gender TEXT,
        age INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
CREATE TABLE study_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        completion_rate REAL NOT NULL,
        accuracy_rate REAL NOT NULL,
        focus_rate REAL NOT NULL,
        score REAL NOT NULL,
        date DATE NOT NULL, knowledge_point TEXT,
        FOREIGN KEY (student_id) REFERENCES students (id)
    );
CREATE TABLE tags (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL
    );
CREATE TABLE task_classes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_id INTEGER NOT NULL,
        class_name TEXT NOT NULL,
        FOREIGN KEY (task_id) REFERENCES tasks (id)
    );
CREATE TABLE task_submissions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_id INTEGER NOT NULL,
        student_id INTEGER NOT NULL,
        score REAL,
        submitted_at TIMESTAMP,
        FOREIGN KEY (task_id) REFERENCES tasks (id),
        FOREIGN KEY (student_id) REFERENCES students (id)
    );
CREATE TABLE tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        creator_id INTEGER NOT NULL,
        paper_id INTEGER,
        due_date TIMESTAMP NOT NULL,
        allow_late_submission BOOLEAN DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (creator_id) REFERENCES users (id),
        FOREIGN KEY (paper_id) REFERENCES papers (id)
    );
CREATE TABLE user_profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL UNIQUE,
            learning_level TEXT,
            study_style TEXT,
            preferred_time TEXT,
            preferred_material_type TEXT,
            attendance_rate REAL DEFAULT 0,
            avg_completion_rate REAL DEFAULT 0,
            avg_accuracy_rate REAL DEFAULT 0,
            avg_focus_rate REAL DEFAULT 0,
            avg_score REAL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        );
CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL,
        name TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    , student_id TEXT, teacher_id TEXT, class_number INTEGER);
INSERT INTO "users" VALUES(1,'admin','123456','admin','???','2025-08-12 04:32:53',NULL,NULL,NULL);
INSERT INTO "users" VALUES(2,'天晨','pbkdf2:sha256:260000$ad38ot0mMy0pIx8J$a0003ae28178a609ada3992791d12f7cf751c3d9de16d776de90f6466d2f38a6','teacher','天晨','2025-08-23 06:50:06',NULL,'20010001',1);
INSERT INTO "users" VALUES(3,'小芳','pbkdf2:sha256:260000$OUNxgNWX8ZXR6Yy5$e34729a2d3add865a71cfc37e25e68cbfcf1772e67471db3dec83110404a0066','student','小芳','2025-08-26 07:06:10','10010001',NULL,1);
INSERT INTO "users" VALUES(4,'小李','pbkdf2:sha256:260000$nnGjdKbEjEQTjoyL$4841ce1f48fd58e7774782769495f317d65005371d1f35ec078b51464709b561','student','小李','2025-08-26 07:09:22','10010002',NULL,1);
INSERT INTO "users" VALUES(5,'小王','pbkdf2:sha256:260000$VqSWIAqHIt1ejHex$0f552d271fa58aaae601e88bdaa00f5666313278c309ef88ac72b486578bdb60','student','小王','2025-08-26 07:09:40','10010003',NULL,1);
INSERT INTO "users" VALUES(6,'小陈','pbkdf2:sha256:260000$gaDRkA9JEaW7JFQS$985f3eb39b26e1c45108d50a93f5ada3d888fa8cc79762527e74000e35d4a3db','student','小陈','2025-08-26 07:09:56','10010004',NULL,1);
INSERT INTO "users" VALUES(7,'小杨','pbkdf2:sha256:260000$rEWiXfmT0tv1IgIP$d85c8b0b82b5cae038eb85b326cf2b273ee31ecb1a4bd9f3d2a2e511b2f80744','student','小杨','2025-08-26 07:10:16','10010005',NULL,1);
INSERT INTO "users" VALUES(8,'小美','pbkdf2:sha256:260000$lUMFpfVX14Ocia1J$e600ddedc240c24e2022382670d86452b6a37c11ccb6a74c067923b1ce2f6a4c','student','小美','2025-08-26 07:10:29','10010006',NULL,1);
INSERT INTO "users" VALUES(9,'张亦林','pbkdf2:sha256:260000$HUWdQbDF8Rvh3d5I$79e8e6a2ed8918618718c73f93bcb573a8d0e763cd299b85b75c0ba453a05fc0','student','张亦林','2025-08-26 07:43:19','10010009',NULL,1);
INSERT INTO "users" VALUES(10,'陈语琪','pbkdf2:sha256:260000$cZebBA3ZiIrPxlaE$10cec73b204ad44504ff9462be56b230ce775b493b2f4148f5fde103c3a66302','student','陈语琪','2025-08-26 07:43:19','10010011',NULL,1);
INSERT INTO "users" VALUES(11,'刘思清','pbkdf2:sha256:260000$SFeLg1SxBAQf48Rg$73da8c9365e1066abb2fee915ea57a1194ac1515e78588aa9de8488f4b7c23d0','student','刘思清','2025-08-26 07:43:19','10010010',NULL,1);
INSERT INTO "users" VALUES(12,'杨梓妍','pbkdf2:sha256:260000$QVp0eeg5E2HoWQ35$99001c7240204ea027bcf81bd622c1c72112bbc1722e6a08e30d380c035375fc','student','杨梓妍','2025-08-26 07:43:19','10010012',NULL,1);
INSERT INTO "users" VALUES(13,'李若怡','pbkdf2:sha256:260000$JUbNp4nr6vBhrsan$7da2d264db65f669fff7b5eee3efd0b9e24da687fbbc51676ac5567314030739','student','李若怡','2025-08-26 07:43:19','10010008',NULL,1);
INSERT INTO "users" VALUES(14,'王子涵','pbkdf2:sha256:260000$OPcDaDcsBU0i3747$e0b037d02234ad711b3ecc02e8ee5661461f14d7af80a3d9de706a83acb28fdb','student','王子涵','2025-08-26 07:43:19','10010007',NULL,1);
INSERT INTO "users" VALUES(15,'黄雨宁','pbkdf2:sha256:260000$foPPkc0OIJLWkKCF$33a34256b96f530b93f8e489efb01dba9f67b9e523b614d1e229b71c13acbe6f','student','黄雨宁','2025-08-26 07:43:20','10010014',NULL,1);
INSERT INTO "users" VALUES(16,'赵子航','pbkdf2:sha256:260000$oaohDlU15vEF20rD$fa7bb6dafadbfa6ac6c061a7e32bf0b632ddb39f1bd31ed9ad1425332414aea7','student','赵子航','2025-08-26 07:43:20','10010013',NULL,1);
INSERT INTO "users" VALUES(17,'吴一昕','pbkdf2:sha256:260000$kiHBbg5pk8v6C6iS$c62125acc803b3c8b8cb193330b29ce72afd5defa9ad094bb43c3971d90f0bd2','student','吴一昕','2025-08-26 07:43:20','10010016',NULL,1);
INSERT INTO "users" VALUES(18,'孙晨博','pbkdf2:sha256:260000$9DA80c2BVC6E51EX$89d0a221b1d388dc28dfb891410bff29df9c2bc538e6ce11cb5107f08a873f85','student','孙晨博','2025-08-26 07:43:20','10010018',NULL,1);
INSERT INTO "users" VALUES(19,'徐明浩','pbkdf2:sha256:260000$3zu6J75E2nOT0Bda$35a660f445f29f6c4405f2f8ee8e833e66dfc0b34579eaea20b9f78146b13582','student','徐明浩','2025-08-26 07:43:20','10010017',NULL,1);
INSERT INTO "users" VALUES(20,'周彦杰','pbkdf2:sha256:260000$tTTbHM7EwnyaEfNZ$cc746fe8be4551b4d58299bbe901bd7f4cc340d4dc93a33394d902631ffafd0c','student','周彦杰','2025-08-26 07:43:20','10010015',NULL,1);
INSERT INTO "users" VALUES(21,'胡可睿','pbkdf2:sha256:260000$TrSEni34FU2U0ucr$82ed6a2c7a39aad197ccfc2f3884227799eca9e61d7c8ad5e5ac773af1a3255a','student','胡可睿','2025-08-26 07:43:20','10010019',NULL,1);
INSERT INTO "users" VALUES(22,'朱浩辰','pbkdf2:sha256:260000$bwqk7jQzjCvFxVkh$85db7c03805ea0ed5b3a1f09a119e5959c3d56a6c0b28cb7ae1e72ee37a2bbfa','student','朱浩辰','2025-08-26 07:43:20','10010020',NULL,1);
INSERT INTO "users" VALUES(23,'林家钧','pbkdf2:sha256:260000$PTC1B3dHFNMigboV$b8f7782fb7b150dd4c084f9f9d1029adf2f646ea0333ef3b6ba502f636215548','student','林家钧','2025-08-26 07:43:20','10010022',NULL,1);
INSERT INTO "users" VALUES(24,'何泽桐','pbkdf2:sha256:260000$viwmSePZMmHju2A1$b87a57d96b60e3826e4e043bad11379c6e87c581d1fb5d721f3ca2897a9b50ca','student','何泽桐','2025-08-26 07:43:20','10010023',NULL,1);
INSERT INTO "users" VALUES(25,'郭钰彤','pbkdf2:sha256:260000$Gbg7He6RC09q76wM$50f61ae8852abb232fca3976e5b38a61e98ad3ce6135a4454686255d9caf6b91','student','郭钰彤','2025-08-26 07:43:20','10010024',NULL,1);
INSERT INTO "users" VALUES(26,'高锦轩','pbkdf2:sha256:260000$RsrGs5QKWL3ZSaEl$d9e18001d4296266d2b34033a91b9977dd040b97b559dbd7b96a55958a433209','student','高锦轩','2025-08-26 07:43:20','10010021',NULL,1);
INSERT INTO "users" VALUES(27,'马宇宸','pbkdf2:sha256:260000$1bFTcRPAAuSnwPzO$c3d4bb0d909c76c7b3ee7f6adb9848b4287f3c7d78dd53f71477a34f0814e1ce','student','马宇宸','2025-08-26 07:43:21','10010025',NULL,1);
INSERT INTO "users" VALUES(28,'罗文阳','pbkdf2:sha256:260000$OXSuqpS3ModUAgVd$fdbf3dc9153adebe3529b6db02e697233449c1615dfd878f3c67bd5423cff102','student','罗文阳','2025-08-26 07:43:21','10010026',NULL,1);
INSERT INTO "users" VALUES(29,'郑乐诺','pbkdf2:sha256:260000$iCs4RzBDLS9CXybG$09de2ce47deda730549ff7e77f6d126a6f688ae4e096d8e373d37a9c5478d313','student','郑乐诺','2025-08-26 07:43:21','10010029',NULL,1);
INSERT INTO "users" VALUES(30,'宋诗然','pbkdf2:sha256:260000$JLhQi15Bg5mO63eb$62a4280cc23ea0c737bd73d180d949ce87d5a517de80c63f34e4d548f4ac2bf3','student','宋诗然','2025-08-26 07:43:21','10010028',NULL,1);
INSERT INTO "users" VALUES(31,'谢欣可','pbkdf2:sha256:260000$QpUseZHTdENcBi0w$8e06280a5322104c48c53ca82235deb2547426ca33e4354c308e2c42d6ad9bf0','student','谢欣可','2025-08-26 07:43:21','10010030',NULL,1);
INSERT INTO "users" VALUES(32,'梁沐豪','pbkdf2:sha256:260000$vMlvM8Fv1SDq3zY8$909e2b1ca4d4ff1e5edd642b4ee5b8c8fcb8b7217ab7624c1c26c4fcb8e3e846','student','梁沐豪','2025-08-26 07:43:21','10010027',NULL,1);
INSERT INTO "users" VALUES(33,'韩子涵','pbkdf2:sha256:260000$DetfnuMl7qpha1xj$892e6f4305c09c2e3ed729a77d1bff442e26c70360ad87fcb997eff62bb2a9da','student','韩子涵','2025-08-26 07:43:21','10010031',NULL,2);
INSERT INTO "users" VALUES(34,'唐若怡','pbkdf2:sha256:260000$WPq9UyNZphTAitHC$b442b5d02c05b16df212626550c6d9ca7552452cd6c60ddae752bc5f1ef8f51f','student','唐若怡','2025-08-26 07:43:21','10010032',NULL,2);
INSERT INTO "users" VALUES(35,'董语琪','pbkdf2:sha256:260000$QoVghxYwq6dzkqM5$fa2aabdad0b8f2fc844baa35df232d8b050f82b64e0886a1a838daa72ae54522','student','董语琪','2025-08-26 07:43:21','10010035',NULL,2);
INSERT INTO "users" VALUES(36,'冯亦林','pbkdf2:sha256:260000$LvpHaHGXWD4jAWwO$f73a0261e160d57836678246adfde12e575e7de1dc65b981327437dc97094a62','student','冯亦林','2025-08-26 07:43:21','10010033',NULL,2);
INSERT INTO "users" VALUES(37,'于思清','pbkdf2:sha256:260000$EVXDfkRaxoEy3jg2$10a2addbc54bfc8bb4861b834a00da93ae3f0037f16bfd9f5a4911636f9d7bd8','student','于思清','2025-08-26 07:43:21','10010034',NULL,2);
INSERT INTO "users" VALUES(38,'萧梓妍','pbkdf2:sha256:260000$pY2zb99Fw27azYON$b2bad98574c62cc7a05b33f64dee1709a30e73184a78206f5abb2a66340e743d','student','萧梓妍','2025-08-26 07:43:21','10010036',NULL,2);
INSERT INTO "users" VALUES(39,'程子航','pbkdf2:sha256:260000$vh1RoHW9hcHlNiDk$cfcc48f3952ba7a8cc949bdfe51eb3f1dd310419ac3ed35d51fd3643962d28af','student','程子航','2025-08-26 07:43:21','10010037',NULL,2);
INSERT INTO "users" VALUES(40,'邓一昕','pbkdf2:sha256:260000$9eJLieDG1P48TAap$a30878853c4ece7a348b544402cc0236380f11fe5d956946cc603f46f4058410','student','邓一昕','2025-08-26 07:43:21','10010040',NULL,2);
INSERT INTO "users" VALUES(41,'许明浩','pbkdf2:sha256:260000$AJilC696wSkx23PS$00dc3dc50c349f6cecaf32449d9f3dd252f043481ab0f74a83d3d7c40760a19c','student','许明浩','2025-08-26 07:43:21','10010041',NULL,2);
INSERT INTO "users" VALUES(42,'袁彦杰','pbkdf2:sha256:260000$cYE9w9Z7jbyoCeZd$ff88bd1c9a48b9883ba3785f7c642e877c4026f2172ab8c970d1e73560084b1b','student','袁彦杰','2025-08-26 07:43:21','10010039',NULL,2);
INSERT INTO "users" VALUES(43,'傅晨博','pbkdf2:sha256:260000$WcVEuNpVzvygAQrS$3866defe255e0721e3581d02133a42184dd6a4b7bd4694583da1708be0a426d0','student','傅晨博','2025-08-26 07:43:21','10010042',NULL,2);
INSERT INTO "users" VALUES(44,'曹雨宁','pbkdf2:sha256:260000$AiDRFTFMycQ1i93I$55f0d9db74c3e02f1b60c188fdb29892148d871e2ce72d01b1f5f940d29fa8da','student','曹雨宁','2025-08-26 07:43:21','10010038',NULL,2);
INSERT INTO "users" VALUES(45,'沈可睿','pbkdf2:sha256:260000$Fc93ICdKOp0HmLBG$58c3fd717339ecc46ff798b89aeb9e6dc5bd8595c6ce8380b070cf5e3ee21eca','student','沈可睿','2025-08-26 07:43:22','10010043',NULL,2);
INSERT INTO "users" VALUES(46,'曾浩辰','pbkdf2:sha256:260000$XtzJOCVfJzxdM2d5$759a1094bb8cd307146a5f92b64b82a4b43ba78b9d1981ad9901efef8e1c2c96','student','曾浩辰','2025-08-26 07:43:22','10010044',NULL,2);
INSERT INTO "users" VALUES(47,'吕家钧','pbkdf2:sha256:260000$0lgD23nwmJDKeAFG$9cef58eb4fd1e0160d87f6ad04369b81e9436ffefface1fec804149e743b7a7b','student','吕家钧','2025-08-26 07:43:22','10010046',NULL,2);
INSERT INTO "users" VALUES(48,'苏泽桐','pbkdf2:sha256:260000$DBNEyDpsd16itRcO$8ff4df43ce6de09ce1db9aae6c54ecbd7f81fbce90f7ef1222d355f685782c23','student','苏泽桐','2025-08-26 07:43:22','10010047',NULL,2);
INSERT INTO "users" VALUES(49,'卢钰彤','pbkdf2:sha256:260000$DOg1FhnDu9raUmVj$35359acf36da88ff65830b7ee031f4ed27f4515d978f55060059cf735e3dc63c','student','卢钰彤','2025-08-26 07:43:22','10010048',NULL,2);
INSERT INTO "users" VALUES(50,'彭锦轩','pbkdf2:sha256:260000$rUnJ4MH5yEjwBFWK$483a1c6c9f597af3c610ce5e552a19e6ffcf6909783b748ad35ba7bf62b22d90','student','彭锦轩','2025-08-26 07:43:22','10010045',NULL,2);
INSERT INTO "users" VALUES(51,'蒋宇宸','pbkdf2:sha256:260000$mAAYgHHokIwrbKHy$80f19f4c98f274a292000f768825637d375e09a69f79d77d66bba2944598e68d','student','蒋宇宸','2025-08-26 07:43:22','10010049',NULL,2);
INSERT INTO "users" VALUES(52,'蔡文阳','pbkdf2:sha256:260000$MoTkm2X2Hk0vSmeT$dd9ac0af2bf7764ef618ec0b192b880d4490b4f76de8476709b517bab6d748af','student','蔡文阳','2025-08-26 07:43:22','10010050',NULL,2);
INSERT INTO "users" VALUES(53,'丁诗然','pbkdf2:sha256:260000$ej1VtJgpiIWyfQFB$4bc9a8aaf4763402b438281bd2209b1109da8bca6a4dcbff638aab389436504e','student','丁诗然','2025-08-26 07:43:22','10010052',NULL,2);
INSERT INTO "users" VALUES(54,'魏乐诺','pbkdf2:sha256:260000$NPhofe0e88NefYYg$02686b63d6edff1dfae719faaf41d7b270867303947874b14b40caaf84c9ed09','student','魏乐诺','2025-08-26 07:43:22','10010053',NULL,2);
INSERT INTO "users" VALUES(55,'薛欣可','pbkdf2:sha256:260000$yPvoSQs0cjwHNt8g$d69a403ad82ac528c1cf99d394454d01bfe530e134b3910012fa647b8b96041f','student','薛欣可','2025-08-26 07:43:22','10010054',NULL,2);
INSERT INTO "users" VALUES(56,'贾沐豪','pbkdf2:sha256:260000$yiiRa57gKoPFnLXg$cdeb4242a27eb23e6631e619ee15a654b1a08513f206eb648dbe59724b2a410f','student','贾沐豪','2025-08-26 07:43:22','10010051',NULL,2);
INSERT INTO "users" VALUES(57,'叶子涵','pbkdf2:sha256:260000$k8qUUkQ9NrN7BNEB$108daf84c6be673267d9bbd645abb1ed7901ae1f5bd554b23d804f5cd098a25e','student','叶子涵','2025-08-26 07:43:23','10010055',NULL,2);
INSERT INTO "users" VALUES(58,'王若怡','pbkdf2:sha256:260000$M0wsJeUCqJ1vVHyk$cb464344a73baca9477534cecf3efac155a21f8d660d07ccacd1ec8ceee5b9de','student','王若怡','2025-08-26 07:43:23','10010056',NULL,2);
INSERT INTO "users" VALUES(59,'张思清','pbkdf2:sha256:260000$d9mWfsZpG9Jd8g9s$f0840f8c6bc0517e8503a1c0a20b21b001ae6cac908667e9e3e57eb40884f199','student','张思清','2025-08-26 07:43:23','10010058',NULL,2);
INSERT INTO "users" VALUES(60,'刘语琪','pbkdf2:sha256:260000$3tWNZON2lpd0vdbb$ce269275f28a377bd8277b9b3b30db15ac8b18ae9a18762b20fd3ef6c39a54d9','student','刘语琪','2025-08-26 07:43:23','10010059',NULL,2);
INSERT INTO "users" VALUES(61,'陈梓妍','pbkdf2:sha256:260000$EsVhMLSXIlom11o0$ed1aa323fa9bf63783a2af3258860fe6f6d94936c08e97a1ca3fac3ae33335e4','student','陈梓妍','2025-08-26 07:43:23','10010060',NULL,2);
INSERT INTO "users" VALUES(62,'李亦林','pbkdf2:sha256:260000$UN1GcMnOp9CTOw89$c46dcee604ecd2e354578d84957f2c132a6bb752f40febd2cc0b54708e1b2bef','student','李亦林','2025-08-26 07:43:23','10010057',NULL,2);
INSERT INTO "users" VALUES(63,'杨子航','pbkdf2:sha256:260000$qwLr5SNzBUg0j1JD$647cb173101ba82a14d306ac7bbd78713c549e8439012a7e8be77865e01d8aa6','student','杨子航','2025-08-26 07:43:23','10010061',NULL,3);
INSERT INTO "users" VALUES(64,'赵雨宁','pbkdf2:sha256:260000$IwdBygmTx27kQvCN$daba9e4d61b4e757d4e5c5d3e1f461edb412a1e837a84f46cc0090cbddd28cc0','student','赵雨宁','2025-08-26 07:43:23','10010062',NULL,3);
INSERT INTO "users" VALUES(65,'周一昕','pbkdf2:sha256:260000$NpZFFUDJ1OmaZxoR$58dd080371c755a893515cf9bd35d04d9f639a553854131177d1247bf1a4aa35','student','周一昕','2025-08-26 07:43:23','10010064',NULL,3);
INSERT INTO "users" VALUES(66,'吴明浩','pbkdf2:sha256:260000$3RvHOvp1njcR3KKA$a30aa60b14049a592c1182f8a614c2ad022002a24de586b7b78f41a029055b80','student','吴明浩','2025-08-26 07:43:23','10010065',NULL,3);
INSERT INTO "users" VALUES(67,'徐晨博','pbkdf2:sha256:260000$sUbWPr91Xcz27FCW$80e5f1da8c37e24bb8b896efc9eca4146d50f74919520399c2d2374196dd34c1','student','徐晨博','2025-08-26 07:43:23','10010066',NULL,3);
INSERT INTO "users" VALUES(68,'黄彦杰','pbkdf2:sha256:260000$JBUu8gBbdPJzxtDs$0478daad3e23183c8811e2e865669e4d41ac1c03ed74b66bd3d3edbfeacfc78f','student','黄彦杰','2025-08-26 07:43:23','10010063',NULL,3);
INSERT INTO "users" VALUES(69,'易天昊','pbkdf2:sha256:260000$UIw39asVCh65rajz$3793c5fb3798899abdda618662c9e72e5ddbd7fd0d1d133e9ad16d6f575df5ca','teacher','易天昊','2025-08-26 07:46:59',NULL,'20010002',1);
INSERT INTO "users" VALUES(70,'鸿若辰','pbkdf2:sha256:260000$oBRyyxjSNVyoegBp$9d52025c93f9936e8bcdd69c6df1898d13d45923052142a3ef3abfe19bfa673e','teacher','鸿若辰','2025-08-26 07:48:09',NULL,'20010003',2);
INSERT INTO "users" VALUES(71,'杨玉佩','pbkdf2:sha256:260000$wg6Fj8Dw0NYXvxj4$4cfdea122d1bbf95a5d531504704e8ae9e212b55b22219dfa6a1e453f73b76c5','teacher','杨玉佩','2025-08-26 07:48:36',NULL,'20010004',2);
CREATE UNIQUE INDEX idx_student_id 
            ON users(student_id) 
            WHERE student_id IS NOT NULL
        ;
CREATE UNIQUE INDEX idx_teacher_id 
            ON users(teacher_id) 
            WHERE teacher_id IS NOT NULL
        ;
CREATE INDEX idx_name_role 
            ON users(name, role)
        ;
CREATE INDEX idx_class_number 
            ON users(class_number) 
            WHERE class_number IS NOT NULL
        ;
CREATE INDEX idx_refresh_tokens_user_id ON refresh_tokens(user_id);
CREATE INDEX idx_refresh_tokens_expires_at ON refresh_tokens(expires_at);
COMMIT;
