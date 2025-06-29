#   D i g i N a t i v a   A I   T e a m   -   A u t o n o m o u s   F e a t u r e   D e v e l o p m e n t   S y s t e m 
 
 # #   <د�  C R I T I C A L :   S t a r t   H e r e 
 
 * * T h i s   r e p o s i t o r y   c o n t a i n s   t h e   A I   t e a m   i n f r a s t r u c t u r e   t h a t   b u i l d s   t h e   D i g i N a t i v a   l e a r n i n g   g a m e   a u t o n o m o u s l y . * * 
 
 # # #   F o r   A I   A s s i s t a n t s   R e a d i n g   T h i s : 
 1 .   * * F I R S T * *   r e a d   ` I m p l e m e n t a t i o n _ r u l e s . m d `   -   i t   c o n t a i n s   A L L   c r i t i c a l   i n f o r m a t i o n 
 2 .   * * T H E N * *   r e a d   ` C L A U D E . m d `   f o r   y o u r   s p e c i f i c   r o l e   a n d   r e s p o n s i b i l i t i e s 
 3 .   * * F I N A L L Y * *   c h e c k   ` d o c s / d n a / `   f o r   p r o j e c t   D N A   t h a t   g u i d e s   a l l   d e c i s i o n s 
 
 # # #   Q u i c k   O v e r v i e w 
 -   * * W h a t * * :   6   s p e c i a l i z e d   A I   a g e n t s   t h a t   b u i l d   f e a t u r e s   f r o m   G i t H u b   i s s u e s   t o   p r o d u c t i o n 
 -   * * H o w * * :   C o n t r a c t - b a s e d   c o m m u n i c a t i o n   w i t h   D N A   v a l i d a t i o n   a t   e v e r y   s t e p 
 -   * * W h e r e * * :   T h i s   r e p o   ( A I   t e a m )   +   s e p a r a t e   p r o d u c t   r e p o   ( g a m e   c o d e ) 
 -   * * W h y * * :   A u t o n o m o u s ,   s c a l a b l e   d e v e l o p m e n t   f o r   S w e d i s h   m u n i c i p a l i t i e s 
 
 # #   =���  R e p o s i t o r y   S t r u c t u r e 
 
 ` ` ` 
 d e v t e a m /                                                 #   T h i s   r e p o s i t o r y   -   A I   T e a m   I n f r a s t r u c t u r e 
 % % %  m o d u l e s /                                         #   C o r e   A I   a g e n t   i m p l e m e n t a t i o n s 
 %      % % %  a g e n t s /                                   #   6   s p e c i a l i z e d   a g e n t s   ( m o d u l a r ) 
 %      %      % % %  p r o j e c t _ m a n a g e r /         #   G i t H u b   �!  S t o r y   b r e a k d o w n 
 %      %      % % %  g a m e _ d e s i g n e r /             #   S t o r y   �!  U X   s p e c i f i c a t i o n 
 %      %      % % %  d e v e l o p e r /                     #   U X   �!  C o d e   i m p l e m e n t a t i o n 
 %      %      % % %  t e s t _ e n g i n e e r /             #   C o d e   �!  T e s t   s u i t e 
 %      %      % % %  q a _ t e s t e r /                     #   T e s t s   �!  U s e r   v a l i d a t i o n 
 %      %      % % %  q u a l i t y _ r e v i e w e r /       #   V a l i d a t i o n   �!  P r o d u c t i o n 
 %      % % %  s h a r e d /                                   #   S h a r e d   c o m p o n e n t s   O N L Y 
 %              % % %  b a s e _ a g e n t . p y               #   B a s e   c l a s s   f o r   a l l   a g e n t s 
 %              % % %  c o n t r a c t _ v a l i d a t o r . p y   #   C o n t r a c t   v a l i d a t i o n 
 %              % % %  s t a t e _ m a n a g e r . p y         #   S t a t e   p e r s i s t e n c e 
 % % %  d o c s /                                               #   C o m p r e h e n s i v e   d o c u m e n t a t i o n 
 %      % % %  d n a /                                         #   P r o j e c t   D N A   ( C R I T I C A L ) 
 %      %      % % %  d e s i g n _ p r i n c i p l e s . m d   #   5   d e s i g n   p r i n c i p l e s 
 %      %      % % %  a r c h i t e c t u r e . m d           #   4   a r c h i t e c t u r e   r u l e s 
 %      %      % % %  t a r g e t _ a u d i e n c e . m d     #   U s e r   p e r s o n a s 
 %      % % %  c o n t r a c t s /                             #   C o n t r a c t   s p e c i f i c a t i o n s 
 % % %  t e s t s /                                             #   T e s t   s u i t e 
 % % %  I m p l e m e n t a t i o n _ r u l e s . m d           #   =ب�  S T A R T   H E R E   -   C o m p l e t e   g u i d e 
 % % %  C L A U D E . m d                                       #   A I   a s s i s t a n t   i n s t r u c t i o n s 
 % % %  R E A D M E . m d                                       #   T h i s   f i l e 
 ` ` ` 
 
 # #   =؀�  Q u i c k   S t a r t 
 
 # # #   P r e r e q u i s i t e s 
 -   P y t h o n   3 . 1 1 + 
 -   N o d e . j s   1 8 +   ( f o r   g a m e   d e v e l o p m e n t ) 
 -   G i t H u b   a c c o u n t   w i t h   r e p o s i t o r y   a c c e s s 
 -   O p e n A I   A P I   k e y   o r   c o m p a t i b l e   L L M 
 
 # # #   I n s t a l l a t i o n 
 
 ` ` ` b a s h 
 #   C l o n e   r e p o s i t o r y 
 g i t   c l o n e   h t t p s : / / g i t h u b . c o m / j h o n n y o 8 8 / d e v t e a m . g i t 
 c d   d e v t e a m 
 
 #   C r e a t e   v i r t u a l   e n v i r o n m e n t 
 p y t h o n   - m   v e n v   v e n v 
 s o u r c e   v e n v / b i n / a c t i v a t e     #   O n   W i n d o w s :   v e n v \ S c r i p t s \ a c t i v a t e 
 
 #   I n s t a l l   d e p e n d e n c i e s 
 p i p   i n s t a l l   - r   r e q u i r e m e n t s . t x t 
 
 #   S e t   u p   e n v i r o n m e n t 
 c p   . e n v . e x a m p l e   . e n v 
 #   E d i t   . e n v   w i t h   y o u r   A P I   k e y s   a n d   c o n f i g u r a t i o n 
 ` ` ` 
 
 # # #   R u n n i n g   t h e   A I   T e a m 
 
 ` ` ` b a s h 
 #   S t a r t   t h e   p r o d u c t i o n   p i p e l i n e 
 p y t h o n   s t a r t _ p r o d u c t i o n _ p i p e l i n e . p y 
 
 #   O r   r u n   s p e c i f i c   a g e n t 
 p y t h o n   - m   m o d u l e s . a g e n t s . p r o j e c t _ m a n a g e r . a g e n t   - - g i t h u b - i s s u e   < i s s u e - u r l > 
 ` ` ` 
 
 # #   =��  K e y   C o n c e p t s 
 
 # # #   1 .   * * C o n t r a c t   S y s t e m * *   ( M O S T   I M P O R T A N T ) 
 E v e r y   a g e n t   c o m m u n i c a t i o n   u s e s   v a l i d a t e d   J S O N   c o n t r a c t s : 
 -   E n a b l e s   m o d u l a r   d e v e l o p m e n t 
 -   P r e v e n t s   t i g h t   c o u p l i n g 
 -   A l l o w s   i n d e p e n d e n t   a g e n t   u p d a t e s 
 -   S e e   ` m o d u l e s / s h a r e d / c o n t r a c t _ v a l i d a t o r . p y ` 
 
 # # #   2 .   * * D N A - D r i v e n   D e v e l o p m e n t * * 
 A l l   d e c i s i o n s   v a l i d a t e d   a g a i n s t   p r o j e c t   D N A : 
 -   5   D e s i g n   P r i n c i p l e s   ( u s e r - f o c u s e d ) 
 -   4   A r c h i t e c t u r e   P r i n c i p l e s   ( t e c h n i c a l ) 
 -   S e e   ` d o c s / d n a / `   f o r   c o m p l e t e   D N A 
 
 # # #   3 .   * * D u a l   R e p o s i t o r y   S t r a t e g y * * 
 -   * * T h i s   r e p o * * :   A I   t e a m   i n f r a s t r u c t u r e 
 -   * * P r o d u c t   r e p o * * :   G a m e   c o d e   a n d   d e p l o y m e n t s 
 -   A g e n t s   c r e a t e   f e a t u r e   b r a n c h e s   i n   p r o d u c t   r e p o 
 -   P r o j e c t   o w n e r   a p p r o v e s   v i a   G i t H u b 
 
 # # #   4 .   * * E v e n t - D r i v e n   A r c h i t e c t u r e * * 
 -   E v e n t B u s   c o o r d i n a t e s   a g e n t   c o m m u n i c a t i o n 
 -   R e a l - t i m e   p r o g r e s s   t r a c k i n g 
 -   A u t o m a t i c   e r r o r   r e c o v e r y 
 -   S e e   ` m o d u l e s / s h a r e d / e v e n t _ b u s . p y ` 
 
 # #   =���  S u c c e s s   M e t r i c s 
 
 T h e   A I   t e a m   o p t i m i z e s   f o r : 
 -   * * C o d e   Q u a l i t y * * :   1 0 0 %   t e s t   c o v e r a g e ,   < 2 0 0 m s   A P I   r e s p o n s e 
 -   * * U s e r   E x p e r i e n c e * * :   > 9 0   L i g h t h o u s e ,   W C A G   A A   c o m p l i a n c e 
 -   * * D e v e l o p m e n t   S p e e d * * :   < 4   h o u r s   p e r   f e a t u r e 
 -   * * D N A   C o m p l i a n c e * * :   > 4 . 0 / 5 . 0   s c o r e   o n   a l l   p r i n c i p l e s 
 
 # #   =����  D e v e l o p m e n t   W o r k f l o w 
 
 1 .   * * C r e a t e   G i t H u b   I s s u e * *   u s i n g   f e a t u r e   t e m p l a t e 
 2 .   * * A I   T e a m   p r o c e s s e s * *   a u t o m a t i c a l l y : 
       -   P r o j e c t   M a n a g e r   a n a l y z e s   a n d   b r e a k s   d o w n 
       -   G a m e   D e s i g n e r   c r e a t e s   U X   s p e c i f i c a t i o n 
       -   D e v e l o p e r   i m p l e m e n t s   c o d e 
       -   T e s t   E n g i n e e r   w r i t e s   t e s t s 
       -   Q A   T e s t e r   v a l i d a t e s   U X 
       -   Q u a l i t y   R e v i e w e r   a p p r o v e s 
 3 .   * * F e a t u r e   b r a n c h   c r e a t e d * *   i n   p r o d u c t   r e p o 
 4 .   * * P r o j e c t   o w n e r   r e v i e w s * *   a n d   a p p r o v e s / r e j e c t s 
 5 .   * * A u t o m a t i c   d e p l o y m e n t * *   o n   a p p r o v a l 
 
 # #   =���  D o c u m e n t a t i o n 
 
 -   ` I m p l e m e n t a t i o n _ r u l e s . m d `   -   C o m p l e t e   i m p l e m e n t a t i o n   g u i d e 
 -   ` C L A U D E . m d `   -   A I   a s s i s t a n t   r o l e   a n d   i n s t r u c t i o n s 
 -   ` d o c s / d n a / `   -   P r o j e c t   D N A   d o c u m e n t s 
 -   ` d o c s / c o n t r a c t s / `   -   C o n t r a c t   s p e c i f i c a t i o n s 
 -   ` d o c s / e n d _ t o _ e n d _ t e s t _ p l a n . m d `   -   T e s t i n g   g u i d e 
 -   ` P R O D U C T I O N _ Q U I C K S T A R T . m d `   -   P r o d u c t i o n   d e p l o y m e n t 
 
 # #   >��  C o n t r i b u t i n g 
 
 T h i s   i s   a n   A I - f i r s t   d e v e l o p m e n t   s y s t e m .   H u m a n   c o n t r i b u t i o n s   s h o u l d   f o c u s   o n : 
 -   I m p r o v i n g   a g e n t   c a p a b i l i t i e s 
 -   E n h a n c i n g   c o n t r a c t   s p e c i f i c a t i o n s 
 -   U p d a t i n g   D N A   p r i n c i p l e s 
 -   F i x i n g   i n f r a s t r u c t u r e   i s s u e s 
 
 # #   =���  L i c e n s e 
 
 P r o p r i e t a r y   -   D i g i N a t i v a   A B .   A l l   r i g h t s   r e s e r v e d . 
 
 - - - 
 
 * * R e m e m b e r * * :   T h e   A I   t e a m ' s   s u c c e s s   d e p e n d s   o n   s t r i c t   c o n t r a c t   c o m p l i a n c e   a n d   D N A   v a l i d a t i o n .   W h e n   i n   d o u b t ,   c o n s u l t   ` I m p l e m e n t a t i o n _ r u l e s . m d ` . 