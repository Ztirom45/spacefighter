if i[self.iteam_pos] and self.iteam_pos:
    img = self.iteam_images[i[self.iteam_pos]-1]
    if self.std_rotozoom != [0,1]:img = pygame.transform.scale(img,(self.std_rotozoom[1]*20,self.std_rotozoom[1]*20))
    if self.scale:img = pygame.transform.rotozoom(img,0,i[self.scale])
    #rect_iteam = img.get_rect()
    #print(20-rect_iteam.w/2)
    pos = (i[self.xy][0]+self.playerx+self.playerpos[0],i[self.xy][1]+self.playery+self.playerpos[1])
    self.screen.blit(img,pos)
    self.screen.blit(self.arial.render(str(i[3]), True, (0,0,0)),(pos[0]+8,pos[1]+28))
    self.screen.blit(self.arial.render(str(i[3]), True, self.font_color),(pos[0]+10,pos[1]+30))

