package com.webbrowsingbot.app;

import org.openqa.selenium.Dimension;
import org.openqa.selenium.Point;

import java.util.ArrayList;
import java.util.Random;
import java.util.TreeMap;

public class Link implements Comparable<Link> {
    private String href;
    private Point location;

    public Dimension getWinSize() {
        return winSize;
    }

    public void setWinSize(Dimension winSize) {
        this.winSize = winSize;
    }

    public double getScore() {
        return score;
    }

    public void setScore(double score) {
        this.score = score;
    }

    private Dimension winSize;
    private double score;

    public String getHref() {
        return href;
    }

    public void setHref(String href) {
        this.href = href;
    }

    public Point getLocation() {
        return location;
    }

    public void setLocation(Point location) {
        this.location = location;
    }

    public Link(String href, Point location, Dimension winSize){
        this.href = href;
        this.location = location;
        this.winSize = winSize;

        calculateScore();
    }

    private void calculateScore(){
        // Calculate middle points of the page
        double midX = winSize.height/2;
        double midY = winSize.width/2;

        // Calculate individual scores
        double scoreX = Math.abs(midX - this.location.getX())/midX;
        double scoreY = Math.abs(midY - this.location.getY())/midY;

        // Invert the score as numbers closer to do the middle should have a higher score (*10 is just for the number to look bigger)
        this.score = (1/(scoreX + scoreY))*10;
    }

    public static Link chooseRandLink(ArrayList<Link> linkArrayList){
        // Weighted random number generator using treemap

        // Map ArrayList into TreeMap
        TreeMap map = new TreeMap<Double, Link>();
        double count = 0.0;
        for(Link l : linkArrayList) { //Just any iterator over all objects
            map.put(count, l);
            count += l.score;
        }

        // Choose random double to get random link
        Random r = new Random();
        double randDouble = (1-r.nextDouble()) * count;

        // Return relevant link
        double key = (double)map.floorKey(randDouble);
        return (Link)map.get(key);

    }

    @Override
    public String toString() {
        return "Link{" +
                "href='" + href + '\'' +
                ", location=" + location +
                ", winSize=" + winSize +
                ", score=" + score +
                '}';
    }

    @Override
    public int compareTo(Link compareTo) {
        double compareAge=((Link)compareTo).getScore();
        return Double.compare(this.score, compareAge);
    }
}
